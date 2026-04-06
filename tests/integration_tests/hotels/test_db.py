from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager


async def test_create_hotel(db: DBManager):
    hotel_data = HotelAdd(title="Hotel 5 Stars", location="Berlin")
    new_hotel_data = await db.hotels.add(hotel_data)
    await db.commit()

    assert new_hotel_data.title == hotel_data.title