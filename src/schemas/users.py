import re
from pydantic import Field, ConfigDict, EmailStr, field_validator
from src.schemas.base import BaseSchema


class UserAddRequest(BaseSchema):
    email: EmailStr
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if len(v) > 254:
            raise ValueError("Email is too long")

        local, domain = v.split("@")

        if len(local) > 64:
            raise ValueError("Email local part is too long")
        if local.startswith(".") or local.endswith("."):
            raise ValueError("Email local part cannot start or end with a dot")
        if ".." in local:
            raise ValueError("Email local part cannot contain consecutive dots")

        if ".." in domain:
            raise ValueError("Email domain cannot contain consecutive dots")

        parts = domain.split(".")
        tld = parts[-1]
        if not tld.isalpha():
            raise ValueError("Invalid TLD in email domain")
        if len(tld) < 2:
            raise ValueError("TLD is too short")

        for part in parts[:-1]:
            if not re.match(r"^[a-zA-Z0-9-]+$", part):
                raise ValueError("Invalid email domain part")
            if not any(c.isalpha() for c in part):
                raise ValueError("Email domain part must contain at least one letter")

        if not re.match(r"^[a-zA-Z0-9.-]+$", domain):
            raise ValueError("Invalid characters in email domain")

        return v.lower()


class UserAdd(BaseSchema):
    email: EmailStr
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    hashed_password: str


class User(BaseSchema):
    id: int
    email: EmailStr
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)

    model_config = ConfigDict(from_attributes=True)


class UserWithHashedPassword(User):
    hashed_password: str
