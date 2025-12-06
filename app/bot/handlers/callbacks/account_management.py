"""Account management callback handlers."""

from seedrcc import AsyncSeedr
from telethon import events

from app.bot.decorators import setup_handler
from app.bot.handlers.commands.accounts import accounts_handler
from app.bot.views.accounts_view import (
    render_account_not_found,
    render_logout_account_confirmation,
    render_no_account,
)
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
        account_to_switch = await account_repo.get_by_id(account_id)

        if not account_to_switch or account_to_switch.user_id != user.id:
            view = render_account_not_found(translator)
            await event.edit(view.message, buttons=view.buttons)
            return

        if user.default_account_id == account_id:
            await event.answer(translator.get("alreadyActive"), alert=False)
            return

        username = account_to_switch.username or account_to_switch.email
        await user_repo.update_settings(user.id, default_account_id=account_to_switch.id)

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
        account = await account_repo.get_by_id(account_id)

        if not account or account.user_id != user.id:
            view = render_account_not_found(translator)
            await event.edit(view.message, buttons=view.buttons)
            return

        username = account.username or account.email
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
        account = await account_repo.get_by_id(account_id)

        if not account or account.user_id != user.id:
            view = render_account_not_found(translator)
            await event.edit(view.message, buttons=view.buttons)
            return

        user_repo = UserRepository(session)
        await account_repo.delete(account_id)
        accounts = await account_repo.get_by_user_id(user.id)
        if user.default_account_id == account_id and accounts:
            await user_repo.update_settings(user.id, default_account_id=accounts[0].id)
        elif not accounts:
            await user_repo.update_settings(user.id, default_account_id=None)
        has_accounts = len(accounts) > 0

    await event.answer(translator.get("accountRemoved"), alert=False)

    if has_accounts:
        await accounts_handler(event)
    else:
        view = render_no_account(translator)
        await event.edit(view.message, buttons=view.buttons)


@setup_handler()
async def cancel_logout_callback(event: events.CallbackQuery.Event, user: User, translator: Translator):
    """Handle cancel logout button - return to accounts view."""
    await event.answer(translator.get("cancelled"), alert=False)
    await accounts_handler(event)
