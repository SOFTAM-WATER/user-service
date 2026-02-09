from fastapi import APIRouter, Depends
from pydantic import UUID4
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_async_session
from app.schemas.user import RegisterUserRequest, UserResponse, LoginUserRequest
from app.api.v1.services.user_service import UserService

router = APIRouter(prefix="/users")


@router.post(
    path="/register",
    status_code=HTTP_201_CREATED,
    response_model=UserResponse
)
async def register(
    user: RegisterUserRequest,
    session: AsyncSession = Depends(get_async_session)
):
    created = await UserService.register(session, user)
    return created


@router.post(
    path="/login",
    status_code=HTTP_200_OK,
    response_model=UserResponse
)
async def login(
    user: LoginUserRequest,
    session: AsyncSession = Depends(get_async_session)
):
    result = await UserService.login(session, user)
    return result