from pydantic import EmailStr
from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.users import UserModel
from src.repositories.mappers.mappers import UserMapper, UserWithHashedPasswordMapper


class UserRepository(BaseRepository):
    model = UserModel
    mapper = UserMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPasswordMapper.map_to_domain_entity(model)
