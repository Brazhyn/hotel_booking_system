from pydantic import ConfigDict, Field, field_validator

from src.schemas.facilities import Facility
from src.schemas.base import BaseSchema
from src.schemas.utils import validate_non_empty


class RoomAddRequest(BaseSchema):
    title: str
    description: str | None = Field(default=None)
    price: int = Field(gt=0)
    quantity: int = Field(ge=0)
    facilities_ids: list[int] | None = Field(default_factory=list)
    
    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        return validate_non_empty(v)
    

class RoomAdd(BaseSchema):
    hotel_id: int
    title: str
    description: str | None = Field(default=None)
    price: int
    quantity: int


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomWithRels(Room):
    facilities: list[Facility]


class RoomPatchRequest(BaseSchema):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None, gt=0)
    quantity: int | None = Field(default=None, ge=0)
    facilities_ids: list[int] | None = Field(default_factory=list)
    
    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        return validate_non_empty(v)


class RoomPatch(BaseSchema):
    hotel_id: int | None = Field(default=None)
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None, gt=0)
    quantity: int | None = Field(default=None, ge=0)
