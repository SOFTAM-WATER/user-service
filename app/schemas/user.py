from uuid import UUID
from datetime import datetime

from fastapi import Query
from pydantic import UUID4, BaseModel, Field

from app.models.user import UserType


class UserID(BaseModel):
    id: UUID4

class UserCreatedAt(BaseModel):
    created_at: datetime

class RegisterUserRequest(BaseModel):
    phone: str = Field(max_length=50)
    telegram_id: int | None = Field()
    full_name: str | None = Field(max_length=50)
    password: str


class LoginUserRequest(BaseModel):
    telegram_id: int | None = Field()
    password: str


class UserResponse(BaseModel):
    id: UUID
    phone: str 
    telegram_id: int | None = None
    full_name: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True

class UserDB(UserID, RegisterUserRequest, UserCreatedAt):
    pass

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        from_attributes = True

class UserCached(BaseModel):
    id: UUID
    phone: str
    telegram_id: int
    full_name: str
    user_type: UserType
    created_at: datetime
    password: str

    class Config:
        from_attributes = True