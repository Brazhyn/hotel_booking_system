from pydantic import BaseModel, Field, ConfigDict, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    password: str


class UserAdd(BaseModel):
    email: EmailStr
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    hashed_password: str


class User(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)

    model_config = ConfigDict(from_attributes=True)


class UserWithHashedPassword(User):
    hashed_password: str
