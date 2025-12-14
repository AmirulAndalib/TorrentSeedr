"""Configuration module for the application."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_prefix="",
    )

    # Telegram Configuration
    telegram_api_id: int = Field(..., description="Telegram API ID from my.telegram.org")
    telegram_api_hash: str = Field(..., description="Telegram API Hash from my.telegram.org")
    telegram_bot_token: str = Field(..., description="Bot token from @BotFather")

    # Database Configuration
    database_url: str = Field(
        default="sqlite:///data/seedrccbot.sqlite",
        description="Database connection URL",
    )

    # Bot Settings
    bot_name: str = Field(default="Seedrcc Bot", description="Name of the bot")
    max_torrent_file_size: int = Field(
        default=1 * 1024 * 1024,  # 1 MB
        description="Maximum allowed size for torrent file uploads in bytes",
    )
    page_size: int = Field(default=8, description="Number of items to show per page in lists")

    # Security
    encryption_key: str = Field(..., description="Fernet encryption key for securing credentials")


# Global settings instance
settings = Settings()
