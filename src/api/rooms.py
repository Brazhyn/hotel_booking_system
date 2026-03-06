from datetime import date

from fastapi import Query, APIRouter

from src.schemas.rooms import RoomAdd, RoomPatchRequest, RoomAddRequest, RoomPatch
from src.api.dependencies import PaginationDep, DBDep
from src.schemas.facilities import RoomFacilityAdd


router = APIRouter(prefix="/hotels", tags=["rooms"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2026-02-26"),
    date_to: date = Query(example="2026-03-02")
):
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to
    )

        
@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    
    
@router.post("/{hotel_id}/rooms")
async def create_room(
    db: DBDep,
    hotel_id: int,
    data: RoomAddRequest,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump(exclude={"facilities_ids"}))
    room = await db.rooms.add(_room_data)
    facilities_ids = data.facilities_ids
    
    room_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in facilities_ids]
    await db.room_facilities.add_bulk(room_facilities_data)
    await db.commit()
    
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    data: RoomAddRequest,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    room = await db.rooms.edit(_room_data, id=room_id, hotel_id=hotel_id)
    
    facilities_ids = data.facilities_ids
    room_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in facilities_ids]
    await db.room_facilities.edit_room_facilities(data=room_facilities_data, room_id=room.id)
    await db.commit()
    
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partial_update_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    data: RoomPatchRequest,
):
    _room_data = RoomPatch(
        hotel_id=hotel_id, 
        **data.model_dump(exclude_unset=True, exclude={"facilities_ids"}))
    
    room = await db.rooms.edit(
        _room_data,
        id=room_id,
        hotel_id=hotel_id,
        exclude_unset=True,
    )
    facilities_ids = data.facilities_ids
    room_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in facilities_ids]
    await db.room_facilities.edit_room_facilities(data=room_facilities_data, room_id=room.id)
    
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}