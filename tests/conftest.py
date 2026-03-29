import json
from typing import AsyncGenerator

from httpx import ASGITransport, AsyncClient
import pytest

from src.main import app
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.models import *
from src.api.dependencies import DBManager
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"
    
    
@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db
        

@pytest.fixture(scope="session", autouse=True)
async def async_main(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)   
        
        
@pytest.fixture(scope="session", autouse=True)
async def add_hotels_and_rooms(async_main):
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
    

@pytest.fixture(scope="session", autouse=True)
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver"
    ) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
async def register_user(async_main, ac):
    response = await ac.post(
        url="/auth/register",
        json={
            "email": "olexandr@2005gmail.com",
            "password": "testpassword"
        }
    )
    data = response.json()["user"]
    
    assert response.status_code == 200
    assert data['email'] == "olexandr@2005gmail.com"
    
        

