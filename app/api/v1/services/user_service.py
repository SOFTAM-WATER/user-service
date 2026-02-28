from uuid import UUID
from starlette.status import HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED

from app.core.errors import AppError
from app.utils.service import BaseService, transaction_mode
from app.schemas.user import RegisterUserRequest, LoginUserRequest, TokenResponse
from app.utils.error_codes import ErrorCode
from app.utils.security import SecurityUtils
from app.database.redis import RedisService
from app.utils.security import SecurityUtils

class UserService(BaseService):
    _repo: str = 'user'

    @transaction_mode
    async def register(self, user_data: RegisterUserRequest):
        existing_user = await self.uow.user.get_by_filter_one_or_none(telegram_id=user_data.telegram_id, phone=user_data.phone)
        if existing_user:
            raise AppError("User already exists", code=ErrorCode.USER_ALREADY_EXISTS, status_code=HTTP_409_CONFLICT)
        
        user_dict = user_data.model_dump()
        user_dict["password"] = SecurityUtils.hash_password(user_dict["password"])

        created_user = await self.uow.user.add_one_and_get_obj(**user_dict)
        return created_user.to_schema()
    
    @transaction_mode
    async def login(self, login_data: LoginUserRequest):
        user = await self.uow.user.get_by_filter_one_or_none(telegram_id=login_data.telegram_id)

        if not user or not SecurityUtils.verify_password(login_data.password, user.password):
            raise AppError("Invalid credentials", ErrorCode.INVALID_CREDENTIALS, HTTP_401_UNAUTHORIZED)
        
        payload = {"sub": str(user.id), "tg_id": getattr(user, "telegram_id", None)}

        access_token = SecurityUtils.create_access_token(payload)
        refresh_token = SecurityUtils.create_refresh_token(payload)

        await RedisService.set_refresh_token(str(user.id), refresh_token)
        await RedisService.set_user(user)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    
    @transaction_mode
    async def get_user_id_by_telegram_id(self, telegram_id: int) -> UUID | None:
        user = await self.uow.user.get_by_filter_one_or_none(telegram_id=telegram_id)

        if not user:
            return None
        return user.id
    
    @transaction_mode
    async def get_user_by_id(self, user_id: UUID):
        user = await self.uow.user.get_by_filter_one_or_none(id=user_id)

        if not user:
            return None
        return user

    @transaction_mode
    async def refresh_token(self, incoming_refresh_token: str):
        payload = SecurityUtils.verify_token(incoming_refresh_token)

        user_id = payload.get("sub")
        if not user_id:
            raise AppError("Invalid token payload", ErrorCode.INVALID_TOKEN, HTTP_401_UNAUTHORIZED)
        
        stored_token = await RedisService.get_refresh_token(user_id)
        if stored_token != incoming_refresh_token:
            raise AppError("Refresh token is invalid or expired", ErrorCode.INVALID_TOKEN, HTTP_401_UNAUTHORIZED)

        new_payload = {"sub": user_id, "tg_id": payload.get("user_id")}

        new_access_token = SecurityUtils.create_access_token(new_payload)
        new_refresh_token = SecurityUtils.create_refresh_token(new_payload)

        await RedisService.set_refresh_token(user_id, new_refresh_token)

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )