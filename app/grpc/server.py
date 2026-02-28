import asyncio, grpc

import app.grpc.generated.user_service_pb2_grpc as user_pb2_grpc
from app.grpc.handlers import UserServiceGrpc
from app.api.v1.deps.uow import uow_factory

async def run_grpc_server() -> None:
    server = grpc.aio.server()
    user_pb2_grpc.add_UserServiceServicer_to_server(
        UserServiceGrpc(uow_factory),
        server
    )

    server.add_insecure_port("[::]:50051")
    await server.start()
    print("🚀 User gRPC server running on 50051")
    
    try:
        await server.wait_for_termination()
    except asyncio.CancelledError:
        print("🛑 gRPC server stopped")