"""Start command handler."""

from telethon import events

from app.bot.decorators import setup_handler
from app.bot.utils.commands import set_user_commands
from app.bot.views.start_view import render_start_message
from app.database.models import User
from app.utils.language import Translator


@setup_handler()
async def start_handler(event: events.NewMessage.Event, user: User, translator: Translator):
    has_accounts = bool(user.default_account_id)

    await set_user_commands(event, translator, has_accounts)

    view = render_start_message(
        has_accounts=has_accounts,
        translator=translator,
    )

    await event.respond(
        view.message,
        buttons=view.buttons,
    )
