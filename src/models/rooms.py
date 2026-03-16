from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.database import Base



class RoomModel(Base):
    __tablename__ = "rooms"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id", ondelete="CASCADE"))
    title: Mapped[str]
    description: Mapped[str | None] = mapped_column(nullable=True)
    price: Mapped[int]
    quantity: Mapped[int]
    
    facilities: Mapped[list["FacilityModel"]] = relationship(
        back_populates="rooms",
        secondary="rooms_facilities"
    )