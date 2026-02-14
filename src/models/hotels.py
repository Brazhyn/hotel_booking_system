from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String 

from src.database import Base



class HotelModel(Base):
    __tablename__ = "hotels"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    location: Mapped[str] 
    
    
