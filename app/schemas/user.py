from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=255, pattern=r"^[A-Za-z_]+$")
    email: EmailStr

    @field_validator("email")
    @classmethod
    def lower_email(cls, value: str) -> str:
        return value.lower()


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=120)

    @field_validator("password")
    @classmethod
    def check_password(cls, value: str) -> str:
        if not value.isascii():
            raise ValueError("password must contain only ASCII characters")
        if not any(ch.isdigit() for ch in value):
            raise ValueError("password must contain a digit")
        if not any(ch.isupper() for ch in value):
            raise ValueError("password must contain an uppercase letter")
        if not any(ch.islower() for ch in value):
            raise ValueError("password must contain a lowercase letter")
        return value


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: int
