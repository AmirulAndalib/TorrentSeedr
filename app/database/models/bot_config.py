from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import Base, TimestampMixin
from app.utils.encryption import EncryptedType


class BotConfig(Base, TimestampMixin):
    """Singleton config table for bot configs."""

    __tablename__ = "bot_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    encryption_canary: Mapped[str | None] = mapped_column(EncryptedType, nullable=True)
