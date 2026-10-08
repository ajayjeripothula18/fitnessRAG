import os
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from dotenv import load_dotenv
from urllib.parse import urlparse
import asyncio
import asyncpg

load_dotenv(os.path.join(os.path.dirname(__file__), "../.env.test"), override=True)

from app.main import app
from app.db.session import Base, get_async_session
from app.models.user import User  # noqa
from app.models.profile import Profile  # noqa
from app.models.conversation import Conversation  # noqa
from app.models.message import Message  # noqa
from app.models.document_chunk import DocumentChunk  # noqa

import os


def _get_test_database_url():
    # Determine the URL: explicit overrides .env.test
    explicit = os.environ.get("TEST_DATABASE_URL")
    if explicit:
        url = explicit
    else:
        user = os.environ.get("POSTGRES_USER", "postgres")
        password = os.environ.get("POSTGRES_PASSWORD", "postgres")
        host = os.environ.get("POSTGRES_SERVER", "db")
        port = os.environ.get("POSTGRES_PORT", "5432")
        db = os.environ.get("POSTGRES_DB", "fitnessrag_test")
        url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
    # Safety: ensure we are using a test database
    parsed = urlparse(url.replace("+asyncpg", ""))  # strip driver for parsing
    db_name = parsed.path.lstrip("/")
    if db_name != "fitnessrag_test":
        raise RuntimeError(
            f"Test database must be 'fitnessrag_test', but got '{db_name}'. "
            "Check your TEST_DATABASE_URL or .env.test."
        )
    return url


def _ensure_test_database_exists(url):
    """Create the test database if it does not exist."""
    parsed = urlparse(url.replace("+asyncpg", ""))  # strip driver for parsing
    db_name = parsed.path.lstrip("/")
    user = parsed.username
    password = parsed.password
    host = parsed.hostname
    port = parsed.port or 5432

    async def _create_if_missing():
        try:
            conn = await asyncpg.connect(
                user=user,
                password=password,
                database="postgres",
                host=host,
                port=port,
            )
            exists = await conn.fetchval(
                "SELECT 1 FROM pg_database WHERE datname = $1", db_name
            )
            if not exists:
                await conn.execute(f'CREATE DATABASE "{db_name}"')
            await conn.close()
        except Exception as e:
            # If we cannot connect, let the original error surface later
            raise

    asyncio.run(_create_if_missing())


TEST_DATABASE_URL = _get_test_database_url()
_ensure_test_database_exists(TEST_DATABASE_URL)

from sqlalchemy.pool import NullPool

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,
)

TestingSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


import asyncio


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    async with test_engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        # Create the trigger function and trigger for content_tsv
        await conn.execute(
            text(
                """
                CREATE OR REPLACE FUNCTION update_document_chunks_content_tsv()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.content_tsv := to_tsvector('english', COALESCE(NEW.content, ''));
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
            """
            )
        )
        await conn.execute(
            text(
                """
                DROP TRIGGER IF EXISTS document_chunks_content_tsv_trigger ON document_chunks;
                """
            )
        )
        await conn.execute(
            text(
                """
                CREATE TRIGGER document_chunks_content_tsv_trigger
                    BEFORE INSERT OR UPDATE OF content
                    ON document_chunks
                    FOR EACH ROW
                    EXECUTE FUNCTION update_document_chunks_content_tsv();
                """
            )
        )
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_async_session():
        yield db_session

    app.dependency_overrides[get_async_session] = override_get_async_session
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()
