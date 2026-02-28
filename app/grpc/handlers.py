import grpc 

import app.grpc.generated.user_service_pb2 as user_pb2
import app.grpc.generated.user_service_pb2_grpc as user_pb2_grpc
from app.api.v1.services.user_service import UserService
from app.database.db import async_session_maker


class UserServiceGrpc(user_pb2_grpc.UserServiceServicer):
    def __init__(self, session_factory):
        self._session_factory = session_factory  

    async def ValidateTelegramUser(self, request, context):
        telegram_id = request.telegram_id
        phone = (request.phone or "").strip()

        if telegram_id <= 0:
            return context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "telegram_id must be positive"
            )

        async with self._session_factory() as session:
            service = UserService(session)
            user_id = await service.get_user_id_by_telegram_id(telegram_id)
            if not user_id:
                return context.abort(
                    grpc.StatusCode.NOT_FOUND,
                    "user not found"
                )

            return user_pb2.ValidateUserResponse(user_id=str(user_id))

