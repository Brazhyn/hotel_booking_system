from pydantic import Field, field_validator
from src.schemas.utils import validate_non_empty
from src.schemas.base import BaseSchema


class HotelAdd(BaseSchema):
    title: str
    location: str

    @field_validator("title", "location")
    @classmethod
    def validate_title_location(cls, v: str) -> str:
        return validate_non_empty(v)


class Hotel(HotelAdd):
    id: int


class HotelPut(BaseSchema):
    title: str
    location: str

    @field_validator("title", "location")
    @classmethod
    def validate_title_location(cls, v: str) -> str:
        return validate_non_empty(v)


class HotelPatch(BaseSchema):
    title: str | None = Field(default=None)
    location: str | None = Field(default=None)

    @field_validator("title", "location")
    @classmethod
    def validate_title_location(cls, v: str) -> str:
        return validate_non_empty(v)
