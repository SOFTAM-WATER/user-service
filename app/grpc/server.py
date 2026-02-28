import asyncio, grpc

import app.grpc.generated.user_service_pb2_grpc as user_pb2_grpc
from app.grpc.handlers import UserServiceGrpc
from app.database.db import async_session_maker

async def run_grpc_server() -> None:
    server = grpc.aio.server()
    user_pb2_grpc.add_UserServiceServicer_to_server(
        UserServiceGrpc(async_session_maker),
        server
    )

    server.add_insecure_port("[::]:50051")
    await server.start()
    print("🚀 gRPC server running on 50051")
    
    try:
        await server.wait_for_termination()
    except asyncio.CancelledError:
        print("🛑 gRPC server stopped")