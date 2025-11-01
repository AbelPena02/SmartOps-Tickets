import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.db import Base, get_db
from app.main import app
from httpx import AsyncClient
from fastapi import Depends

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=True, future=True)
TestSessionLocal = sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(scope="function")
async def db_session():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def client(db_session):
    async def override_get_db():
        async with db_session as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
