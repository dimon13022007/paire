from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy import select

from database.engine import async_sessions
from database.metod_for_database import MetodSQL
from database.models import RegisterUser

def get_logger():
    from main import logger
    return logger

class AutoActivateMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        user = getattr(event, 'from_user', None)
        if user:
            try:
                async with async_sessions() as session:
                    result = await session.execute(
                        select(RegisterUser.is_active).where(RegisterUser.user_name == user.id)
                    )
                    is_active = result.scalar_one_or_none()

                    if is_active is False:
                        await MetodSQL.set_profile_active(user.id, True)

            except Exception as e:
                get_logger().error(f"[AutoActivateMiddleware] Ошибка: {e}")

        return await handler(event, data)
