from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.schemas.user import RegisterUserRequest, UserResponse, LoginUserRequest, TokenResponse
from app.api.v1.deps.services import get_user_service
from app.api.v1.deps.auth import get_current_user
from app.api.v1.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

@router.post(
    path="/register",
    status_code=HTTP_201_CREATED,
    response_model=UserResponse   
)
async def register(
    user: RegisterUserRequest,
    service: UserService = Depends(get_user_service)
):
    created_user = await service.register(user)
    return created_user


@router.post(
    path="/login",
    status_code=HTTP_200_OK,
    response_model=TokenResponse
)
async def login(
    user: LoginUserRequest,
    service: UserService = Depends(get_user_service)
):
    tokens = await service.login(user)
    return tokens


# ------------------------------------


@router.get(
    path="/me",
    status_code=HTTP_200_OK,
    response_model=UserResponse
)
async def get_me(
    user: UserResponse = Depends(get_current_user)
):
    return user