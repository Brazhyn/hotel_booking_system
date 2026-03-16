from src.repositories.base import BaseRepository
from src.models.bookings import BookingModel
from src.repositories.mappers.mappers import BookingMapper


class BookingRepository(BaseRepository):
    model = BookingModel
    mapper = BookingMapper
    