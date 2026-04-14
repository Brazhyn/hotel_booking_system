from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.schemas.facilities import FacilityAddRequest
from src.api.dependencies import DBDep
from src.services.facilities import FacilityService


router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    facilities = await FacilityService(db).get_all_facilities()
    return {"status": "OK", "data": facilities}


@router.post("")
async def create_facility(
    db: DBDep,
    data: FacilityAddRequest = Body(),
):
    facility = await FacilityService(db).create_facility(data)
    return {"status": "OK", "data": facility}
