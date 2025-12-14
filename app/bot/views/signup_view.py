"""Views for signup command."""

from telethon import Button

from app.bot.views import ViewResponse
from app.utils.language import Translator


def render_signup_message(translator: Translator) -> ViewResponse:
    message = translator.get("signupMessage")
    buttons = [[Button.url(translator.get("signupBtn"), "https://www.seedr.cc")]]
    return ViewResponse(message=message, buttons=buttons)
