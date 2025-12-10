"""Main entry point for the bot."""

import asyncio

from structlog import get_logger
from telethon import events

from app.bot.client import bot
from app.bot.handlers.callbacks.account_management import (
    cancel_logout_callback,
    confirm_logout_account_callback,
    logout_account_callback,
    switch_account_callback,
)
from app.bot.handlers.callbacks.active_downloads import (
    active_download_callback,
    cancel_download_callback,
)
from app.bot.handlers.callbacks.delete import (
    delete_file_callback,
    delete_folder_callback,
)
from app.bot.handlers.callbacks.device_auth import (
    auth_complete_callback,
    authorize_device_callback,
)
from app.bot.handlers.callbacks.email_auth import login_email_callback
from app.bot.handlers.callbacks.link import file_link_callback, folder_link_callback
from app.bot.handlers.callbacks.navigation import file_callback, folder_callback
from app.bot.handlers.callbacks.playlist import playlist_callback
from app.bot.handlers.commands.accounts import accounts_handler
from app.bot.handlers.commands.active import active_handler
from app.bot.handlers.messages.add_torrent import add_torrent_handler, handle_torrent_file
from app.bot.handlers.commands.files import files_handler
from app.bot.handlers.commands.info import info_handler
from app.bot.handlers.commands.login import login_handler
from app.bot.handlers.commands.signup import signup_handler
from app.bot.handlers.commands.start import start_handler
from app.bot.handlers.messages.text_message import text_message_handler
from app.config import settings
from app.database import close_db, init_db

logger = get_logger(__name__)


async def main():
    """Main function to start the bot."""
    logger.info(f"Starting {settings.bot_name}")

    # Initialize database
    logger.info("Initializing database")
    await init_db()

    # Start the bot
    logger.info("Connecting to Telegram")
    await bot.start(bot_token=settings.telegram_bot_token)  # type: ignore[]

    # Register handlers
    logger.info("Registering handlers")

    # Command handlers
    bot.add_event_handler(start_handler, events.NewMessage(pattern="/start"))
    bot.add_event_handler(login_handler, events.NewMessage(pattern="/login"))
    bot.add_event_handler(signup_handler, events.NewMessage(pattern="/signup"))
    bot.add_event_handler(info_handler, events.NewMessage(pattern="/info"))
    bot.add_event_handler(accounts_handler, events.NewMessage(pattern="/accounts"))
    bot.add_event_handler(files_handler, events.NewMessage(pattern="/files"))
    bot.add_event_handler(active_handler, events.NewMessage(pattern="/active"))
    bot.add_event_handler(add_torrent_handler, events.NewMessage(pattern=r"(?s).*magnet:\?xt=[^\s]+.*"))

    # Callback handlers - Account
    bot.add_event_handler(authorize_device_callback, events.CallbackQuery(pattern=b"authorize_device"))
    bot.add_event_handler(login_email_callback, events.CallbackQuery(pattern=b"login_email"))
    bot.add_event_handler(auth_complete_callback, events.CallbackQuery(pattern=b"auth_complete_.*"))
    bot.add_event_handler(login_handler, events.CallbackQuery(pattern=b"^login$"))
    bot.add_event_handler(switch_account_callback, events.CallbackQuery(pattern=b"switch_account_.*"))
    bot.add_event_handler(logout_account_callback, events.CallbackQuery(pattern=b"logout_account_.*"))
    bot.add_event_handler(confirm_logout_account_callback, events.CallbackQuery(pattern=b"confirm_logout_.*"))
    bot.add_event_handler(cancel_logout_callback, events.CallbackQuery(pattern=b"cancel_logout"))

    # Callback handlers - Files
    bot.add_event_handler(folder_callback, events.CallbackQuery(pattern=b"folder_(?!link_).*"))
    bot.add_event_handler(folder_link_callback, events.CallbackQuery(pattern=b"folder_link_.*"))
    bot.add_event_handler(file_callback, events.CallbackQuery(pattern=b"file_(?!link_).*"))
    bot.add_event_handler(file_link_callback, events.CallbackQuery(pattern=b"file_link_.*"))
    bot.add_event_handler(delete_file_callback, events.CallbackQuery(pattern=b"delete_file_.*"))
    bot.add_event_handler(delete_folder_callback, events.CallbackQuery(pattern=b"delete_folder_.*"))

    # Callback handlers - Playlist
    bot.add_event_handler(playlist_callback, events.CallbackQuery(pattern=b"playlist_.*"))

    # Callback handlers - Active Downloads
    bot.add_event_handler(active_download_callback, events.CallbackQuery(pattern=b"active_.*"))
    bot.add_event_handler(cancel_download_callback, events.CallbackQuery(pattern=b"cancel_download_.*"))

    # File upload handler (must be before the text_message_handler)
    bot.add_event_handler(
        handle_torrent_file,
        events.NewMessage(
            func=lambda e: e.document
            and (e.document.mime_type == "application/x-bittorrent" or e.file.name.endswith(".torrent"))
        ),
    )

    # This handler catches text button clicks and other text messages.
    bot.add_event_handler(text_message_handler, events.NewMessage(incoming=True))

    logger.info("Bot is running. Press Ctrl+C to stop.")
    await bot.run_until_disconnected()


async def shutdown():
    logger.info("Shutting down")
    await close_db()
    await bot.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down.")
        asyncio.run(shutdown())
    except Exception as e:
        logger.error("A fatal error occurred", error=str(e), exc_info=True)
        asyncio.run(shutdown())
