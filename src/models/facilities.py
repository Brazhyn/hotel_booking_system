from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.database import Base


class FacilityModel(Base):
    __tablename__ = "facilities"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    
    rooms: Mapped[list["RoomModel"]] = relationship(
        back_populates="facilities",
        secondary="rooms_facilities"
    )
    

class RoomFacilityModel(Base):
    __tablename__ = "rooms_facilities"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"))
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id", ondelete="CASCADE"))