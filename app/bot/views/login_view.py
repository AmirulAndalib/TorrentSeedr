"""Views for login management."""

from telethon import Button

from app.bot.views import ViewResponse
from app.utils.language import Translator


def render_login_message(translator: Translator) -> ViewResponse:
    "Render view for /login"
    message = translator.get("loginMessage")
    buttons = [
        [
            Button.inline(
                translator.get("loginWithEmailBtn"),
                b"login_email",
            )
        ],
        [
            Button.inline(
                translator.get("authorizeWithDeviceBtn"),
                b"authorize_device",
            )
        ],
    ]
    return ViewResponse(message=message, buttons=buttons)
