"""Signup command handler."""

from telethon import events

from app.bot.decorators import setup_handler
from app.bot.views.signup_view import render_signup_message
from app.database.models import User
from app.utils.language import Translator


@setup_handler()
async def signup_handler(
    event: events.NewMessage.Event | events.CallbackQuery.Event, user: User, translator: Translator
):
    """Handle both /signup command and signup callback."""
    view = render_signup_message(translator)

    if isinstance(event, events.CallbackQuery.Event):
        await event.edit(view.message, buttons=view.buttons, link_preview=False)
    else:
        await event.respond(view.message, buttons=view.buttons, link_preview=False)
