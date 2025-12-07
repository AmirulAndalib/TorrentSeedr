"""Email and password authentication callback handlers."""

from seedrcc import AsyncSeedr
from seedrcc.exceptions import AuthenticationError
from telethon import events

from app.bot.client import bot
from app.bot.decorators import setup_handler
from app.bot.views.login_view import (
    render_enter_email,
    render_enter_password_for,
    render_incorrect_password,
    render_logged_in,
    render_logging_in,
)
from app.bot.views.start_view import render_start_message
from app.database import get_session
from app.database.models import User
from app.database.repository import AccountRepository, UserRepository
from app.utils.language import Translator


@setup_handler()
async def login_email_callback(event: events.CallbackQuery.Event, user: User, translator: Translator):
    """Handle email/password login callback."""
    try:
        cancel_text = translator.get("cancelBtn")

        async with bot.conversation(user.telegram_id, timeout=300) as conv:
            # Prompt for email address
            view = render_enter_email(translator)
            await conv.send_message(view.message, buttons=view.buttons)

            # After getting email response
            email_response = await conv.get_response()
            email = email_response.text.strip()

            if email == cancel_text:
                view = render_start_message(has_accounts=bool(user.default_account_id), translator=translator)
                await conv.send_message(translator.get("cancelled"), buttons=view.buttons)
                conv.cancel()
                raise events.StopPropagation()

            await email_response.delete()

            # Prompt for password
            view = render_enter_password_for(email, translator)
            await conv.send_message(view.message, buttons=view.buttons)

            # After getting password response
            password_response = await conv.get_response()
            password = password_response.text.strip()

            if password == cancel_text:
                view = render_start_message(has_accounts=bool(user.default_account_id), translator=translator)
                await conv.send_message(translator.get("cancelled"), buttons=view.buttons)
                conv.cancel()
                raise events.StopPropagation()

            await password_response.delete()

            view = render_logging_in(translator)
            status_message = await conv.send_message(view.message, buttons=view.buttons)

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
                    password=password,
                    is_premium=bool(settings.account.premium),
                    invites_remaining=settings.account.invites,
                )
                await UserRepository(session).update_settings(user.id, default_account_id=account.id)

            view = render_logged_in(settings.account.username, translator)
            await status_message.edit(view.message, buttons=view.buttons)

    except TimeoutError:
        await event.respond(translator.get("conversationTimeout"))
    except AuthenticationError:
        view = render_incorrect_password(translator)
        await event.respond(view.message, buttons=view.buttons)
