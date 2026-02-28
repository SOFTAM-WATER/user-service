from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError
from typing import Any

from starlette.status import HTTP_401_UNAUTHORIZED

from app.core.config import get_settings
from app.core.errors import AppError
from app.utils.error_codes import ErrorCode


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 
settings = get_settings()


class SecurityUtils:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)


    @staticmethod
    def verify_password(plain_password: str, hash_password: str) -> bool:
        return pwd_context.verify(plain_password, hash_password)
    

    @staticmethod
    def create_access_token(data: dict[str, Any]) -> str:
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    

    @staticmethod
    def create_refresh_token(data: dict[str, Any]) -> str:
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"}) 
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    

    @staticmethod
    def verify_token(token: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)

            if payload.get("sub") is None:
                raise AppError(
                    "Token payload is invalid: misssing subject",
                    ErrorCode.INVALID_TOKEN,
                    HTTP_401_UNAUTHORIZED
                )
            
            return payload
        
        except JWTError as e:
            raise AppError(
                "Could not validate credentials or token expired",
                ErrorCode.INVALID_TOKEN,
                HTTP_401_UNAUTHORIZED
            )
    
