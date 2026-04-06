from fastapi import APIRouter, Body, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.repositories.users import UserRepository
from src.schemas.users import UserRequestAdd, UserAdd
from src.database import async_session_maker
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authorization and authentication"])


@router.post("/login")
async def login_user(
    db: DBDep,
    response: Response,
    data: UserRequestAdd = Body(openapi_examples={
        "1": {
            "summary": "Yurii", "value": {
                "email": "yura95@gmail.com",
                "password": "yura_123"
            }
        }    
    }),
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="User with this email isn't registered!")
    if not AuthService().verify_password(plain_password=data.password, hashed_password=user.hashed_password):
        raise HTTPException(status_code=401, detail="Password is incorrect")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/register") 
async def register_user(
    db: DBDep,
    data: UserRequestAdd = Body(openapi_examples={
        "1": {"summary": "Bohdan", "value": {
            "email": "alex730@gmail.com",
            "first_name": "Alex",
            "last_name": "Pereira",
            "password": "alex_123",
        }},
    })
):
    try:
        hashed_password = AuthService().hashed_password(data.password)
        new_user_data = UserAdd(
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name,
            hashed_password=hashed_password
        )
        user = await db.users.add(new_user_data)
        await db.commit()
    except:
        raise HTTPException(status_code=400)
    return {"status": "OK"}


@router.post("/logout")
def logout_user(
    response: Response,
):
    response.delete_cookie("access_token")
    return {"status": "OK"}


@router.get("/me")
async def get_me(
    db: DBDep,
    user_id: UserIdDep, 
):
    user = await db.users.get_one_or_none(id=user_id)
    return user
    
    