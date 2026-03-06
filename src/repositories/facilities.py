from src.repositories.base import BaseRepository
from src.models.facilities import FacilitityModel, RoomFacilityModel
from src.schemas.facilities import Facility, RoomFacility


class FacilityRepository(BaseRepository):
    model = FacilitityModel
    schema = Facility
    

class RoomFacilityRepository(BaseRepository):
    model = RoomFacilityModel
    schema = RoomFacility
    