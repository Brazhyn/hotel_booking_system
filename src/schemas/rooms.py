from pydantic import BaseModel, ConfigDict, Field


class RoomRequestAdd(BaseModel):
    title: str
    description: str | None = Field(default=None)
    price: int
    quantity: int
    
    
class RoomAdd(RoomRequestAdd):
    hotel_id: int

    
class Room(RoomAdd):
    id: int 
    hotel_id: int
    
    model_config = ConfigDict(from_attributes=True)
    

class RoomPatch(BaseModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None)
    quantity: int | None = Field(default=None)