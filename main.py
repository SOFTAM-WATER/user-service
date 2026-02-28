import asyncio
from enum import Enum
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import app.models.user
from app.database.db import engine, Base
from app.api.v1.routers.auth import router as auth_router
from app.grpc.server import run_grpc_server
from app.core.errors import AppError
from scripts.init_models import init_models

@asynccontextmanager
async def lifespan(app: FastAPI):
    grpc_task = asyncio.create_task(run_grpc_server())
    await init_models(engine)

    yield

    grpc_task.cancel()

    try:
        await grpc_task
    except asyncio.CancelledError:
        pass


app = FastAPI(lifespan=lifespan)

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    code = exc.code.value if isinstance(exc.code, Enum) else exc.code

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": code,
            "message": exc.message,
            "details": exc.details if exc.details else "no details"
        }
    )

app.include_router(auth_router)