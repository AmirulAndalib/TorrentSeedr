"""Database session management."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from structlog import get_logger

from app.config import settings
from app.database.models import Base
from app.database.models.bot_config import BotConfig

logger = get_logger(__name__)


def make_async_db_url(db_url: str) -> str:
    """Converts a DB URL to URL with SQLAlchemy async engines."""
    url = make_url(db_url)

    driver_map = {
        "sqlite": "sqlite+aiosqlite",
        "postgresql": "postgresql+asyncpg",
        "postgres": "postgresql+asyncpg",
    }

    if url.drivername in driver_map:
        url = url.set(drivername=driver_map[url.drivername])

    return url.render_as_string(hide_password=False)


# Create async engine
engine = create_async_engine(
    make_async_db_url(settings.database_url),
    pool_size=20,
    max_overflow=30,
    pool_timeout=10,
    pool_recycle=1800,
    pool_pre_ping=True,
    echo=False,
    future=True,
)

# Create session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession]:
    """Get async database session.

    Usage:
        async with get_session() as session:
            # Use session here
            result = await session.execute(...)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database tables."""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Close database connections."""
    await engine.dispose()


async def validate_encryption_key() -> None:
    """Validate that ENCRYPTION_KEY can decrypt existing data."""

    async with AsyncSessionLocal() as session:
        encryption_canary = "NEVER GONNA GIVE YOU UP, NEVER GONNA LET YOU DOWN"
        try:
            config = await session.get(BotConfig, 1)
        except Exception as e:
            logger.critical(
                "ENCRYPTION KEY VALIDATION FAILED: "
                "The encryption key does not match the one provided during bot initialization."
            )
            raise RuntimeError(
                "Cannot decrypt existing data with provided ENCRYPTION_KEY. "
                "Application startup aborted to prevent data corruption."
            ) from e

        # Config does not exist yet
        if config is None:
            config = BotConfig(id=1, encryption_canary=encryption_canary)
            session.add(config)
            await session.commit()
            logger.info("Created encryption canary")
            return

        # Config exists but encryption_canary is not set
        elif config.encryption_canary is None:
            config.encryption_canary = encryption_canary
            await session.commit()
            logger.info("Initialized encryption canary")
            return
