from fastapi import APIRouter, Body

from src.schemas.facilities import FacilityAddRequest
from src.api.dependencies import DBDep


router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()
    

@router.post("")
async def create_facility(
    db: DBDep,
    data: FacilityAddRequest = Body(),
):
    facility = await db.facilities.add(data)
    await db.commit()
    return {"status": "OK", "data": facility}
