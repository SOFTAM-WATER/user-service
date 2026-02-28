from fastapi import Depends
from starlette.status import HTTP_404_NOT_FOUND
from fastapi.security import OAuth2PasswordBearer

from app.core.errors import AppError
from app.database.redis import RedisService
from app.api.v1.services.user_service import UserService
from app.api.v1.deps.services import get_user_service
from app.utils.security import SecurityUtils
from app.utils.error_codes import ErrorCode


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service)
):
    payload = SecurityUtils.verify_token(token)
    user_id = payload.get("sub")

    cached_user = await RedisService.get_user(user_id)
    if cached_user:
        return cached_user

    db_user = await service.get_user_by_id(user_id)
    if not db_user:
        raise AppError("User not Found", ErrorCode.USER_NOT_FOUND, HTTP_404_NOT_FOUND)
    
    return db_user
    