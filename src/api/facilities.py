from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.schemas.facilities import FacilityAddRequest
from src.api.dependencies import DBDep


router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    facilities =  await db.facilities.get_all()
    return {"status": "OK", "data": facilities}


@router.post("")
async def create_facility(
    db: DBDep,
    data: FacilityAddRequest = Body(),
):
    facility = await db.facilities.add(data)
    await db.commit()
    
    return {"status": "OK", "data": facility}
