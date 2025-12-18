from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings
from app.core.db.base import Base


settings = get_settings()

print("🔥 SESSION DATABASE_URL =", settings.database_url) 

def get_engine() -> AsyncEngine:
    """
    Create the async SQLAlchemy engine.
    """

    return create_async_engine(str(settings.database_url), echo=False, future=True)


engine: AsyncEngine = get_engine()

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that yields an async DB session.
    """

    async with AsyncSessionLocal() as session:
        yield session


__all__ = ["Base", "engine", "AsyncSessionLocal", "get_db_session"]


