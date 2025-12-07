"""Device authorization callback handlers."""

from seedrcc import AsyncSeedr
from seedrcc.exceptions import AuthenticationError
from telethon import events

from app.bot.decorators import setup_handler
from app.bot.views.login_view import (
    render_auth_failed,
    render_authorize_device,
    render_logged_in,
    render_logging_in,
)
from app.database import get_session
from app.database.models import User
from app.database.repository import AccountRepository, UserRepository
from app.utils.language import Translator


@setup_handler()
async def authorize_device_callback(event: events.CallbackQuery.Event, user: User, translator: Translator):
    """Handle device authorization start callback."""
    device_data = await AsyncSeedr.get_device_code()
    view = render_authorize_device(device_data.device_code, device_data.user_code, translator)
    await event.edit(view.message, buttons=view.buttons, link_preview=False)


@setup_handler()
async def auth_complete_callback(event: events.CallbackQuery.Event, user: User, translator: Translator):
    """Handle authorization completion callback."""
    device_code = event.data.decode().replace("auth_complete_", "")

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

            await UserRepository(session).update_settings(user.id, default_account_id=account.id)

        view = render_logged_in(settings.account.username, translator)
        await event.edit(view.message, buttons=view.buttons)
    except AuthenticationError as e:
        if e.error_type == "authorization_pending":
            await event.answer(translator.get("authPending"), alert=True)
            return
        view = render_auth_failed(str(e), translator)
        await event.edit(view.message, buttons=view.buttons)
