from datetime import datetime
from datetime import timedelta, timezone
from fastapi import HTTPException
from passlib.context import CryptContext
import jwt

from src.adapters.protocols import LoginResponseProtocol
from src.exceptions import (
    ObjectAlreadyExistsException,
    UserAlreadyExistsException,
    ObjectNotFoundException,
    UserNotFoundException,
    InvalidPasswordException,
    EmptyPasswordException,
    InvalidTokenException
)
from src.config import settings
from src.services.base import BaseService
from src.schemas.users import UserAddRequest, UserAdd


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def register_user(self, data: UserAddRequest):
        if not data.password or not data.password.strip():
            raise EmptyPasswordException
            
        hashed_password = self.hashed_password(data.password)
        new_user_data = UserAdd(
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name,
            hashed_password=hashed_password,
        )
        try:
            await self.db.users.add(new_user_data)
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex
        await self.db.commit()

    async def login_user(self, response: LoginResponseProtocol, data: UserAddRequest):
        try:
            user = await self.db.users.get_user_with_hashed_password(email=data.email)
        except ObjectNotFoundException:
            raise UserNotFoundException
        if not self.verify_password(
            plain_password=data.password, hashed_password=user.hashed_password
        ):
            raise InvalidPasswordException
        access_token = self.create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return access_token

    async def logout_user(self, response: LoginResponseProtocol):
        response.delete_cookie("access_token")

    async def get_me(self, user_id: int):
        try:
            return await self.db.users.get_one(id=user_id)
        except ObjectNotFoundException:
            raise UserNotFoundException

    def hashed_password(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.InvalidTokenError:
            raise InvalidTokenException
