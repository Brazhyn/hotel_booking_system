from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class UserModel(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    first_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(200))
