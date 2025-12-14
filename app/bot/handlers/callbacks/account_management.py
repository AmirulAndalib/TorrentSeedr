"""Account management callback handlers."""

from seedrcc import AsyncSeedr
from telethon import events

from app.bot.decorators import setup_handler
from app.bot.handlers.commands.accounts import accounts_handler
from app.bot.views.accounts_view import (
    render_account_not_found,
    render_logout_account_confirmation,
)
from app.bot.views.start_view import render_start_message
from app.database import get_session
from app.database.models import User
from app.database.repository import AccountRepository, UserRepository
from app.utils.language import Translator


@setup_handler(require_auth=True)
async def switch_account_callback(
    event: events.CallbackQuery.Event,
    user: User,
    translator: Translator,
    seedr_client: AsyncSeedr,
):
    """Handle switch to specific account callback."""
    callback_data = event.data.decode()
    account_id = int(callback_data.replace("switch_account_", ""))

    async with get_session() as session:
        user_repo = UserRepository(session)
        account_repo = AccountRepository(session)
        account_to_switch = await account_repo.get_by_id(account_id, user.id)

    if not account_to_switch:
        view = render_account_not_found(translator)
        await event.edit(view.message, buttons=view.buttons)
        return

    if user.default_account_id == account_id:
        await event.answer(translator.get("alreadyActive"), alert=False)
        return

    username = account_to_switch.username or account_to_switch.email
    await user_repo.update_settings(event, user.id, default_account_id=account_to_switch.id)

    await event.answer(translator.get("accountSwitched").format(username=username), alert=False)
    await accounts_handler(event)


@setup_handler(require_auth=True)
async def logout_account_callback(
    event: events.CallbackQuery.Event, user: User, translator: Translator, seedr_client: AsyncSeedr
):
    """Handle logout account button - show confirmation."""
    callback_data = event.data.decode()
    account_id = int(callback_data.replace("logout_account_", ""))

    async with get_session() as session:
        account_repo = AccountRepository(session)
        account = await account_repo.get_by_id(account_id, user.id)

        if not account:
            view = render_account_not_found(translator)
            await event.edit(view.message, buttons=view.buttons)
            return

        username = account.username or account.email or ""
        view = render_logout_account_confirmation(account_id, username, translator)
        await event.edit(view.message, buttons=view.buttons)


@setup_handler(require_auth=True)
async def confirm_logout_account_callback(
    event: events.CallbackQuery.Event, user: User, translator: Translator, seedr_client: AsyncSeedr
):
    """Handle confirmed account logout."""
    callback_data = event.data.decode()
    account_id = int(callback_data.replace("confirm_logout_", ""))

    async with get_session() as session:
        account_repo = AccountRepository(session)
        account = await account_repo.get_by_id(account_id, user.id)

        if not account:
            view = render_account_not_found(translator)
            await event.edit(view.message, buttons=view.buttons)
            return

        user_repo = UserRepository(session)

        # Get all accounts before deletion
        accounts = await account_repo.get_by_user_id(user.id)
        has_multiple_accounts = len(accounts) >= 2

        # Delete the account
        await account_repo.delete(account_id, user.id)

        # Update default account if the deleted account was the default
        if user.default_account_id == account_id:
            if has_multiple_accounts:
                new_default = next((acc for acc in accounts if acc.id != account_id), None)
                if new_default:
                    await user_repo.update_settings(event, user.id, default_account_id=new_default.id)
            else:
                # Only one account (being deleted), set to None
                await user_repo.update_settings(event, user.id, default_account_id=None)

    await event.answer(translator.get("accountRemoved"), alert=False)

    if has_multiple_accounts:
        await accounts_handler(event)
    else:
        view = render_start_message(False, translator)
        await event.edit(view.message, buttons=view.buttons)


@setup_handler()
async def cancel_logout_callback(event: events.CallbackQuery.Event, user: User, translator: Translator):
    """Handle cancel logout button - return to accounts view."""
    await accounts_handler(event)
