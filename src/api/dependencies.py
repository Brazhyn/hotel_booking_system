from typing import Annotated

from fastapi import Query, Depends
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, ge=1)]
    per_page: Annotated[int, Query(5, ge=1, lt=30)]
    
    
PaginationDep = Annotated[PaginationParams, Depends()]