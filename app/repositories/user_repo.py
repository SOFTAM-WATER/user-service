from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

class UserRepository():
    @staticmethod
    async def create_user(session: AsyncSession, **kwargs):
        user = User(**kwargs)
        session.add(user)

        await session.flush()
        return user
    
    @staticmethod
    async def get_by_phone(session: AsyncSession, phone: str):
        stmt = select(User).where(User.phone == phone)
        user = (await session.execute(stmt)).scalar_one_or_none()

        return user