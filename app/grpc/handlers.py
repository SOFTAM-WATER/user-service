import grpc 

import app.grpc.generated.user_service_pb2 as user_pb2
import app.grpc.generated.user_service_pb2_grpc as user_pb2_grpc
from app.repositories.user_repo import UserRepository
from app.database.db import async_session_maker


class UserServiceGrpc(user_pb2_grpc.UserServiceServicer):
    def __init__(self, session_factory):
        self._session_factory = session_factory  

    async def ValidateTelegramUser(self, request, context):
        telegram_id = request.telegram_id
        phone = (request.phone or "").strip()

        if telegram_id <= 0:
            return user_pb2.ValidateUserResponse(user_id="", status=user_pb2.INVALID_DATA)

        async with self._session_factory() as session:
            user = await UserRepository.get_by_telegram_id(session, telegram_id)

            if not user:
                return user_pb2.ValidateUserResponse(user_id="", status=user_pb2.NOT_FOUND)

            return user_pb2.ValidateUserResponse(user_id=str(user.id), status=user_pb2.VALID)

