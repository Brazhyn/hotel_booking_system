from src.services.base import BaseService
from src.schemas.facilities import FacilityAddRequest


class FacilityService(BaseService):
    async def get_all_facilities(self):
        return await self.db.facilities.get_all()

    async def create_facility(self, data: FacilityAddRequest):
        facility = await self.db.facilities.add(data)
        await self.db.commit()

        return facility
