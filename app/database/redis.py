from redis import asyncio as aioredis

from app.core.config import get_settings
from app.models.user import User
from app.schemas.user import UserCached


settings = get_settings()
redis_client = aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)


class RedisService:
    @staticmethod
    async def set_refresh_token(user_id: str, token: str, expire_days: int = 7):
        await redis_client.set(
            f"refresh_token:{user_id}",
            token,
            ex=expire_days*24*60*60
        )


    @staticmethod
    async def get_refresh_token(user_id: str) -> str | None:
        return await redis_client.get(f"refresh_token:{user_id}")
    

    @staticmethod
    async def delete_refresh_token(user_id: str) -> None:
        await redis_client.delete(f"refresh_token:{user_id}")


    @staticmethod
    async def set_user(user: User, expire: int = 900):
        try:
            user_schema = UserCached.model_validate(user)
            user_json = user_schema.model_dump_json()

            await redis_client.set(
                f"user:{user.id}",
                user_json,
                ex=expire
            )

        except Exception as e:
            print(f"Redis cache error: {e}")
    

    @staticmethod
    async def get_user(user_id: str) -> UserCached | None:
        try:
            user_json = await redis_client.get(f"user:{user_id}")

            if not user_json:
                return None
            
            return UserCached.model_validate_json(user_json)
        
        except Exception as e:
            print(f"Redis cache error: {e}")

    
    @staticmethod
    async def delete_user(user_id: str):
        await redis_client.delete(f"user:{user_id}")
            