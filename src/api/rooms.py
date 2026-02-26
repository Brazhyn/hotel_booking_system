import asyncio
from fastapi import Body, APIRouter

from src.schemas.rooms import Room, RoomAdd, RoomPatch, RoomRequestAdd
from src.repositories.rooms import RoomRepository
from src.api.dependencies import PaginationDep
from src.database import async_session_maker


router = APIRouter(prefix="/hotels", tags=["rooms"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    pagination: PaginationDep,
):
    async with async_session_maker() as session:
        per_page = pagination.per_page or 5
        return await RoomRepository(session).get_all(
            hotel_id=hotel_id,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )
        
        
@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
    hotel_id: int,
    room_id: int,
):
    async with async_session_maker() as session:
        return await RoomRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)
    
    
@router.post("/{hotel_id}/rooms")
async def create_room(
    hotel_id: int,
    data: RoomRequestAdd,
):
    async with async_session_maker() as session:
        room_dict = data.model_dump()
        room_dict["hotel_id"] = hotel_id
        room = await RoomRepository(session).add(RoomAdd(**room_dict))
        await session.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(
    hotel_id: int,
    room_id: int,
    data: RoomPatch,
):
    async with async_session_maker() as session:
        await RoomRepository(session).edit(data, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partial_update_room(
    hotel_id: int,
    room_id: int,
    data: RoomPatch,
):
    async with async_session_maker() as session:
        await RoomRepository(session).edit(
            data,
            id=room_id,
            hotel_id=hotel_id,
            exclude_unset=True,
        )
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    hotel_id: int,
    room_id: int,
):
    async with async_session_maker() as session:
        await RoomRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}