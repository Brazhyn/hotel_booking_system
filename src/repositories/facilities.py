from sqlalchemy import select, delete, insert

from src.repositories.base import BaseRepository
from src.models.facilities import FacilitityModel, RoomFacilityModel
from src.schemas.facilities import Facility, RoomFacility, RoomFacilityAdd


class FacilityRepository(BaseRepository):
    model = FacilitityModel
    schema = Facility
    

class RoomFacilityRepository(BaseRepository):
    model = RoomFacilityModel
    schema = RoomFacility
    
    async def edit_room_facilities(self, data: list[RoomFacilityAdd], room_id):
        query = select(self.model.facility_id).filter_by(room_id=room_id)
        result = await self.session.execute(query)
        
        f_ids_existing = set(result.scalars().all())
        f_ids_incoming = set([room_facility.facility_id for room_facility in data])
        
        ids_to_delete = list(f_ids_existing - f_ids_incoming)
        ids_to_add = list(f_ids_incoming - f_ids_existing)
        
        if ids_to_delete:
            await self.session.execute(
                delete(self.model).filter(
                    self.model.room_id == room_id,
                    self.model.facility_id.in_(ids_to_delete)
                )
            )
        if ids_to_add:
            await self.session.execute(
                insert(self.model).values(
                    [
                        {
                            "room_id": room_id,
                            "facility_id": f_id
                        }
                        for f_id in ids_to_add
                    ]
                )
            )
        

        
        
        
        
        
        
        
        
        
        
        
        
    
    