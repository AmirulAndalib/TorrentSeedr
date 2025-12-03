from seedrcc import AsyncSeedr
from seedrcc.exceptions import AuthenticationError
from telethon import events

from app.bot.client import bot
from app.bot.decorators import setup_handler
from app.bot.handlers.commands.accounts import accounts_handler
from app.bot.views.info_view import (
    render_account_not_found,
    render_auth_failed,
    render_authorize_device,
    render_enter_email,
    render_enter_password_for,
    render_incorrect_password,
    render_logged_in,
    render_logging_in,
    render_logout_account_confirmation,
    render_no_account,
)
from app.database import get_session
from app.database.models import Account, User
from app.database.repository import AccountRepository, UserRepository
from app.utils.language import Translator


@setup_handler(require_auth=True)
async def switch_account_callback(
    event: events.CallbackQuery.Event,
    user: User,
    translator: Translator,
    seedr_client: AsyncSeedr,
    db_account: Account,
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

        username = (
            account_to_switch.username
            or account_to_switch.email
            or f"Account {account_to_switch.id}"
        )
        await user_repo.update_settings(user.id, default_account_id=account_to_switch.id)

    await event.answer(translator.get("accountSwitched").format(username=username), alert=False)

    await accounts_handler(event)


@setup_handler(require_auth=True)
async def delete_account_callback(
    event: events.CallbackQuery.Event, user: User, translator: Translator, db_account: Account
):
    """Handle delete account button - show confirmation."""
    callback_data = event.data.decode()
    account_id = int(callback_data.replace("delete_account_", ""))

    if db_account.id != account_id:
        view = render_account_not_found(translator)
        await event.edit(view.message, buttons=view.buttons)
        return

    username = db_account.username or db_account.email or f"Account {db_account.id}"
    view = render_logout_account_confirmation(account_id, username, translator)
    await event.edit(view.message, buttons=view.buttons)


@setup_handler(require_auth=True)
async def confirm_delete_account_callback(
    event: events.CallbackQuery.Event, user: User, translator: Translator, db_account: Account
):
    """Handle confirmed account deletion."""
    callback_data = event.data.decode()
    account_id = int(callback_data.replace("confirm_delete_", ""))

    if db_account.id != account_id:
        view = render_account_not_found(translator)
        await event.edit(view.message, buttons=view.buttons)
        return

    has_accounts = False
    async with get_session() as session:
        user_repo = UserRepository(session)
        account_repo = AccountRepository(session)
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
async def cancel_delete_callback(
    event: events.CallbackQuery.Event, user: User, translator: Translator
):
    """Handle cancel delete button - return to accounts view."""
    await event.answer(translator.get("cancelled"), alert=False)
    await accounts_handler(event)


@setup_handler()
async def login_email_callback(
    event: events.CallbackQuery.Event, user: User, translator: Translator
):
    """Handle email/password login start callback."""
    try:
        await event.answer()
        async with bot.conversation(user.telegram_id, timeout=300) as conv:
            view = render_enter_email(translator)
            await conv.send_message(view.message, buttons=view.buttons)

            email_response = await conv.get_response()
            email = email_response.text.strip()
            await email_response.delete()

            view = render_enter_password_for(email, translator)
            await conv.send_message(view.message, buttons=view.buttons)

            password_response = await conv.get_response()
            password = password_response.text.strip()
            await password_response.delete()

            view = render_logging_in(translator)
            status_message = await conv.send_message(view.message, buttons=view.buttons)

            # Direct call to AsyncSeedr
            seedr_client = await AsyncSeedr.from_password(email, password)
            token = seedr_client.token
            settings = await seedr_client.get_settings()

            async with get_session() as session:
                account_repo = AccountRepository(session)
                account = await account_repo.create(
                    user_id=user.id,
                    seedr_account_id=str(settings.account.user_id),
                    token=token.to_base64(),
                    username=settings.account.username,
                    email=email,
                    password=password,  # Note: Consider security implications of storing passwords
                    is_premium=bool(settings.account.premium),
                    invites_remaining=settings.account.invites,
                )
                accounts = await account_repo.get_by_user_id(user.id)
                if len(accounts) == 1:
                    await UserRepository(session).update_settings(
                        user.id, default_account_id=account.id
                    )

            view = render_logged_in(settings.account.username, len(accounts), translator)
            await status_message.edit(view.message, buttons=view.buttons)

    except TimeoutError:
        await event.respond(translator.get("conversationTimeout"))
    except AuthenticationError:
        view = render_incorrect_password(translator)
        await conv.send_message(view.message, buttons=view.buttons)
    finally:
        await event.delete()


@setup_handler()
async def authorize_device_callback(
    event: events.CallbackQuery.Event, user: User, translator: Translator
):
    """Handle device authorization start callback."""
    # Direct call to AsyncSeedr.get_device_code
    device_data = await AsyncSeedr.get_device_code()
    view = render_authorize_device(device_data.device_code, device_data.user_code, translator)
    await event.edit(view.message, buttons=view.buttons, link_preview=False)


@setup_handler()
async def auth_complete_callback(
    event: events.CallbackQuery.Event, user: User, translator: Translator
):
    """Handle authorization completion callback."""
    device_code = event.data.decode().replace("auth_complete_", "")
    view = render_logging_in(translator)
    await event.edit(view.message, buttons=view.buttons)

    try:
        seedr_client = await AsyncSeedr.from_device_code(device_code)
        token = seedr_client.token
        settings = await seedr_client.get_settings()

        async with get_session() as session:
            account_repo = AccountRepository(session)
            account = await account_repo.create(
                user_id=user.id,
                seedr_account_id=str(settings.account.user_id),
                token=token.to_base64(),
                username=settings.account.username,
                email=settings.account.email,
                is_premium=bool(settings.account.premium),
                invites_remaining=settings.account.invites,
            )
            accounts = await account_repo.get_by_user_id(user.id)
            if len(accounts) == 1:
                await UserRepository(session).update_settings(
                    user.id, default_account_id=account.id
                )

        view = render_logged_in(settings.account.username, len(accounts), translator)
        await event.edit(view.message, buttons=view.buttons)
    except AuthenticationError as e:
        view = render_auth_failed(str(e), translator)
        await event.edit(view.message, buttons=view.buttons)


@setup_handler()
async def login_callback(event: events.CallbackQuery.Event, user: User, translator: Translator):
    """Handle the generic 'login' callback to reuse login_handler logic."""
    from app.bot.handlers.commands.login import (
        login_handler,  # Import here to avoid circular dependency
    )

    await login_handler(event, user=user, translator=translator)
