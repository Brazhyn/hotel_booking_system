from pydantic import BaseModel, ConfigDict


class FacilityAddRequest(BaseModel):
    title: str


class Facility(BaseModel):
    id: int
    title: str

    model_config = ConfigDict(from_attributes=True)


class RoomFacilityAdd(BaseModel):
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
