"""Views for signup command."""

from textwrap import dedent

from telethon import Button

from app.bot.views import ViewResponse
from app.utils.language import Translator


def render_signup_message(translator: Translator) -> ViewResponse:
    message = dedent(f"""
        <b>{translator.get("signupBtn")}</b>

        {translator.get("signupMessage")}
    """)
    buttons = [[Button.url(translator.get("createAccountBtn"), "https://www.seedr.cc")]]
    return ViewResponse(message=message.strip(), buttons=buttons)
