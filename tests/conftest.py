# ruff: noqa: E402, F403
import asyncio
import sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # for windows
import json
from typing import AsyncGenerator
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from httpx import ASGITransport, AsyncClient
import pytest

from src.main import app
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.models import *
from src.api.dependencies import DBManager, get_db
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, None]:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session")
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def add_hotels_and_rooms(setup_database):
    with open("tests/mock_hotels.json", "r") as f_h:
        hotels_data = json.load(f_h)
    with open("tests/mock_rooms.json", "r") as f_r:
        rooms_data = json.load(f_r)

    hotels_schema_list = [HotelAdd.model_validate(hotel) for hotel in hotels_data]
    rooms_schema_list = [RoomAdd.model_validate(room) for room in rooms_data]
    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        hotels = await db_.hotels.add_bulk(hotels_schema_list)
        rooms = await db_.rooms.add_bulk(rooms_schema_list)
        await db_.commit()

    assert hotels
    assert rooms


@pytest.fixture(scope="session")
async def ac(add_hotels_and_rooms) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        yield client


@pytest.fixture(scope="session")
async def register_user(setup_database, ac):
    response = await ac.post(
        url="api/v1/auth/register",
        json={"email": "olexandr@2005gmail.com", "password": "testpassword"},
    )

    assert response.status_code == 200


@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac):
    response = await ac.post(
        url="api/v1/auth/login",
        json={"email": "olexandr@2005gmail.com", "password": "testpassword"},
    )
    access_token = response.json()["access_token"]

    assert ac.cookies.get("access_token") == access_token
    yield ac
