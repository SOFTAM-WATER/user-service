from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError
from app.repositories.user_repo import UserRepository
from app.utils.hash import hash_password, verify_password
from app.utils.error_codes import ErrorCode

class UserService():
    @staticmethod
    async def register(session: AsyncSession, data):
        try:
            user = await UserRepository.create_user(
                session, 
                phone = data.phone,
                telegram_id = data.telegram_id,
                full_name = data.full_name,
                password = hash_password(data.password)
            )

            await session.commit()
            await session.refresh(user)
            return user

        except IntegrityError:
            await session.rollback()
            raise AppError(
                message="A user with this phone number or telegram_id already exists.",
                code=ErrorCode.USER_ALREADY_EXISTS,
                status_code=409
            )
        
    
    @staticmethod
    async def login(session: AsyncSession, data):
        user = await UserRepository.get_by_phone(session, data.phone)

        if user is None or not verify_password(data.password, user.password):
            raise AppError(
                message="You entered an incorrect phone or password.",
                code=ErrorCode.INVALID_PHONE_OR_PASSWORD,
                status_code=401
            )
            
        return user    