from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.exceptions import ObjectNotFoundException
from src.repositories.base import BaseRepository
from src.models.users import UserModel
from src.repositories.mappers.mappers import UserMapper, UserWithHashedPasswordMapper


class UserRepository(BaseRepository):
    model = UserModel
    mapper = UserMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return UserWithHashedPasswordMapper.map_to_domain_entity(model)
