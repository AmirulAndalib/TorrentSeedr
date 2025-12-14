"""Message handlers for incoming text messages from reply keyboard."""

from telethon import events

from app.bot.decorators import setup_handler
from app.bot.handlers.commands.accounts import accounts_handler
from app.bot.handlers.commands.active import active_handler
from app.bot.handlers.commands.files import files_handler
from app.bot.handlers.commands.info import info_handler
from app.bot.handlers.commands.login import login_handler
from app.bot.handlers.commands.signup import signup_handler
from app.bot.handlers.commands.start import start_handler
from app.database.models import User
from app.utils.language import Translator


@setup_handler(require_auth=False)
async def text_message_handler(event: events.NewMessage.Event, user: User, translator: Translator, **kwargs):
    """
    Handles text messages from reply keyboard buttons.
    """
    text = event.message.text

    # Map button text to the corresponding handler function.
    actions = {
        translator.get("fileManagerBtn"): files_handler,
        translator.get("activeDownloadsBtn"): active_handler,
        translator.get("infoBtn"): info_handler,
        translator.get("accountsBtn"): accounts_handler,
        translator.get("loginBtn"): login_handler,
        translator.get("signupBtn"): signup_handler,
    }

    handler = actions.get(text)
    if handler:
        # Call the respective handler
        await handler(event, user=user)
    else:
        await start_handler(event, user=user, translator=translator)
