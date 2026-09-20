from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from sqlalchemy import create_engine
from app.core.config import settings
from typing import AsyncGenerator, Generator

# ---------------------------------------------------------------------------
# Async engine — used by FastAPI auth/user endpoints
# ---------------------------------------------------------------------------
ASYNC_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

engine = create_async_engine(ASYNC_DATABASE_URL, echo=settings.DEBUG, future=True)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


# ---------------------------------------------------------------------------
# Sync engine — used by LangGraph pipeline (synchronous invocation)
# ---------------------------------------------------------------------------
SYNC_DATABASE_URL = (
    f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

sync_engine = create_engine(SYNC_DATABASE_URL, echo=settings.DEBUG, future=True)

SyncSessionLocal = sessionmaker(sync_engine, class_=Session, expire_on_commit=False)


def get_sync_session() -> Generator[Session, None, None]:
    """Sync DB session for use in LangGraph pipeline and background tasks."""
    with SyncSessionLocal() as session:
        yield session
