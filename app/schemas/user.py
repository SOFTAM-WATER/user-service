from datetime import datetime

from fastapi import Query
from pydantic import UUID4, BaseModel, Field
from uuid import UUID

class UserID(BaseModel):
    id: UUID4


class RegisterUserRequest(BaseModel):
    phone: str = Field(max_length=50)
    telegram_id: int | None = Field()
    full_name: str | None = Field(max_length=50)
    password: str


class LoginUserRequest(BaseModel):
    phone: str = Field(max_length=100)
    password: str


class UserResponse(BaseModel):
    id: UUID
    phone: str 
    telegram_id: int | None = None
    full_name: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True