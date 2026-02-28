from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.utils.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository[User]):
    _model = User