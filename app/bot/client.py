"""Telethon bot client initialization."""

from telethon import TelegramClient

from app.config import settings


def create_bot() -> TelegramClient:
    """Create and configure the Telethon bot client.

    Returns:
        TelegramClient: Configured Telethon client instance
    """
    bot = TelegramClient(
        session=".telethon_authentication.session",
        api_id=settings.telegram_api_id,
        api_hash=settings.telegram_api_hash,
    )
    bot.parse_mode = "html"

    return bot


bot = create_bot()
