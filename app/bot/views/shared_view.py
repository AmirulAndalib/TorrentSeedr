"""Shared view components for the bot."""

from telethon import Button

from app.utils.language import Translator


def get_main_keyboard(has_accounts: bool, translator: Translator) -> list:
    """Get the main keyboard buttons."""
    if has_accounts:
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
        keyboard = [
            [
                Button.text(translator.get("loginBtn"), resize=True),
                Button.text(translator.get("signupBtn"), resize=True),
            ],
        ]
    return keyboard
