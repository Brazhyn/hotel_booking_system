from fastapi import APIRouter, Body, Response

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import UserAddRequest
from src.services.auth import AuthService
from src.exceptions import (
    UserAlreadyExistsException,
    UserAlreadyExistsHTTPException,
    UserNotFoundException,
    UserNotFoundHTTPException,
    InvalidPasswordException,
    InvalidPasswordHTTPException,
    EmptyPasswordException,
    ValidationHTTPException
)

router = APIRouter(prefix="/auth", tags=["Authorization and authentication"])


@router.post("/login")
async def login_user(
    db: DBDep,
    response: Response,
    data: UserAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Yurii",
                "value": {"email": "yura95@gmail.com", "password": "yura_123"},
            }
        }
    ),
):
    try:
        access_token = await AuthService(db).login_user(response, data)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except InvalidPasswordException:
        raise InvalidPasswordHTTPException

    return {"access_token": access_token}


@router.post("/register")
async def register_user(
    db: DBDep,
    data: UserAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Bohdan",
                "value": {
                    "email": "alex730@gmail.com",
                    "first_name": "Alex",
                    "last_name": "Pereira",
                    "password": "alex_123",
                },
            },
        }
    ),
):
    try:
        await AuthService(db).register_user(data)
    except EmptyPasswordException as ex:
        raise ValidationHTTPException(detail=ex.detail)
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException
    return {"status": "OK"}


@router.post("/logout")
async def logout_user(
    user_id: UserIdDep,
    response: Response,
):
    await AuthService().logout_user(response)
    return {"status": "OK"}


@router.get("/me")
async def get_me(
    db: DBDep,
    user_id: UserIdDep,
):
    try:
        return await AuthService(db).get_me(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
