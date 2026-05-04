from pydantic import ConfigDict, field_validator

from src.schemas.utils import validate_non_empty
from src.schemas.base import BaseSchema


class FacilityAddRequest(BaseSchema):
    title: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        return validate_non_empty(v)


class Facility(BaseSchema):
    id: int
    title: str

    model_config = ConfigDict(from_attributes=True)


class RoomFacilityAdd(BaseSchema):
    """
    Schema with ready-to-add data into repository
    """

    room_id: int
    facility_id: int


class RoomFacility(RoomFacilityAdd):
    """
    Schema for creating domain objects
    """

    id: int

    model_config = ConfigDict(from_attributes=True)
