from typing import Annotated

from fastapi import HTTPException, Query, Depends, Request
from pydantic import BaseModel

from src.services.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, ge=1)]
    per_page: Annotated[int, Query(5, ge=1, lt=30)]
    
    
def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="There is no authentication token!")
    return token

    
def get_current_user_id(
    token: str = Depends(get_token)
) -> int:
    data = AuthService().decode_token(token)
    user_id = data.get("user_id")
    return user_id

    
PaginationDep = Annotated[PaginationParams, Depends()]
UserIdDep = Annotated[int, Depends(get_current_user_id)]

