"""Views for /start command."""

from telethon import Button

from app.bot.views import ViewResponse
from app.utils.language import Translator


def render_start_message(has_accounts: bool, translator: Translator) -> ViewResponse:
    if has_accounts:
        message = translator.get("greet")
        keyboard = [
            [
                Button.text(translator.get("fileManagerBtn"), resize=True),
                Button.text(translator.get("activeDownloadsBtn"), resize=True),
            ],
            [
                Button.text(translator.get("infoBtn"), resize=True),
                Button.text(translator.get("accountsBtn"), resize=True),
            ],
        ]
    else:
        message = translator.get("welcomeMessage")
        keyboard = [
            [
                Button.text(translator.get("loginBtn"), resize=True),
                Button.text(translator.get("signupBtn"), resize=True),
            ],
        ]

    return ViewResponse(message=message, buttons=keyboard)
