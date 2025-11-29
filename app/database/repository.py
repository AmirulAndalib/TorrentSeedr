"""Repository for database operations."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Account, User


class UserRepository:
    """Repository for User operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        """Get user by Telegram ID."""
        result = await self.session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        """Get user by ID."""
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create(
        self,
        telegram_id: int,
        username: str | None = None,
        language: str = "en",
    ) -> User:
        """Create a new user."""
        user = User(
            telegram_id=telegram_id,
            username=username,
            language=language,
        )
        self.session.add(user)
        await self.session.flush()
        return user

    async def update_settings(
        self,
        user_id: int,
        language: str | None = None,
        playlist_format: str | None = None,
        default_account_id: int | None = None,
    ) -> User | None:
        """Update user settings."""
        user = await self.get_by_id(user_id)
        if not user:
            return None

        if language is not None:
            user.language = language
        if playlist_format is not None:
            user.playlist_format = playlist_format
        if default_account_id is not None:
            user.default_account_id = default_account_id

        await self.session.flush()
        return user

    async def get_or_create(self, telegram_id: int, username: str | None = None) -> User:
        """Get user or create if not exists."""
        user = await self.get_by_telegram_id(telegram_id)
        if not user:
            user = await self.create(telegram_id, username)
        return user


class AccountRepository:
    """Repository for Account operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, account_id: int) -> Account | None:
        """Get account by ID."""
        result = await self.session.execute(select(Account).where(Account.id == account_id))
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> list[Account]:
        """Get all accounts for a user."""
        result = await self.session.execute(
            select(Account).where(Account.user_id == user_id).order_by(Account.created_at)
        )
        return list(result.scalars().all())

    async def create(
        self,
        user_id: int,
        seedr_account_id: str,
        token: str,
        username: str | None = None,
        email: str | None = None,
        password: str | None = None,
        cookie: str | None = None,
        is_premium: bool = False,
        invites_remaining: int = 0,
    ) -> Account:
        """Create a new account."""
        account = Account(
            user_id=user_id,
            seedr_account_id=seedr_account_id,
            token=token,
            username=username,
            email=email,
            password=password,
            cookie=cookie,
            is_premium=is_premium,
            invites_remaining=invites_remaining,
        )
        self.session.add(account)
        await self.session.flush()
        return account

    async def update_token(self, account_id: int, token: str) -> Account | None:
        """Update account token."""
        account = await self.get_by_id(account_id)
        if not account:
            return None

        account.token = token
        await self.session.flush()
        return account

    async def delete(self, account_id: int) -> bool:
        """Delete an account."""
        account = await self.get_by_id(account_id)
        if not account:
            return False

        await self.session.delete(account)
        await self.session.flush()
        return True
