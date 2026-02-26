from src.repositories.base import BaseRepository
from src.models.rooms import RoomModel


class HotelRepository(BaseRepository):
    model = RoomModel

    