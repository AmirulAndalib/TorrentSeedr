"""Account model for storing Seedr account information."""

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base, TimestampMixin
from app.utils.encryption import EncryptedType

if TYPE_CHECKING:
    from app.database.models.user import User


class Account(Base, TimestampMixin):
    __tablename__ = "accounts"
    __table_args__ = (
        UniqueConstraint("seedr_account_id", "user_id", name="uq_seedr_account_user"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    # Seedr account details
    seedr_account_id: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    invites_remaining: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Authentication tokens (encrypted)
    token: Mapped[str] = mapped_column(EncryptedType, nullable=False)
    password: Mapped[str | None] = mapped_column(EncryptedType, nullable=True)
    cookie: Mapped[str | None] = mapped_column(EncryptedType, nullable=True)

    # Relationships
    user: Mapped[User] = relationship("User", back_populates="accounts")

    def __repr__(self) -> str:
        return f"<Account(id={self.id}, seedr_account_id={self.seedr_account_id}, user_id={self.user_id})>"
