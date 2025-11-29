"""Start command handler."""

from telethon import events

from app.bot.decorators import setup_handler
from app.bot.views.start_view import render_start_message
from app.database import get_session
from app.database.models import User
from app.database.repository import AccountRepository
from app.utils.language import Translator


@setup_handler()
async def start_handler(event: events.NewMessage.Event, user: User, translator: Translator):
    async with get_session() as session:
        accounts = await AccountRepository(session).get_by_user_id(user.id)

    view = render_start_message(
        has_accounts=len(accounts) > 0,
        translator=translator,
    )

    await event.respond(
        view.message,
        buttons=view.buttons,
    )
