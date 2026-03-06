from src.repositories.base import BaseRepository
from src.models.bookings import BookingModel
from src.schemas.bookings import Booking


class BookingRepository(BaseRepository):
    model = BookingModel
    schema = Booking
    