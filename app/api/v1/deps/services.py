from fastapi import Depends

from app.api.v1.services.user_service import UserService
from app.utils.unit_of_work import UnitOfWork 

async def get_user_service(uow: UnitOfWork = Depends()) -> UserService:
    return UserService(uow=uow)