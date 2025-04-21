import logging
from aiogram.types import BufferedInputFile
from aio.bot_token import bot

from sqlalchemy.future import select
from database.session import async_session
from database.models import Advertisement


logger = logging.getLogger(__name__)

async def get_image(image_path: str):
    try:
        return BufferedInputFile(image_path, filename="profile.jpg")
    except Exception as e:
        logger.error(f"Ошибка при загрузке изображения {image_path}: {e}")
        return None

async def send_advertisement(chat_id: int):
    try:
        async with async_session() as session:
            ad = await session.scalar(select(Advertisement).order_by(Advertisement.id.desc()).limit(1))
            if not ad:
                return

            if ad.image_path:
                img = await get_image(ad.image_path)
                if img:
                    await bot.send_photo(chat_id, photo=img, caption=ad.text)
                    return

            await bot.send_message(chat_id, ad.text)

    except Exception as e:
        logger.error(f"Ошибка при отправке рекламы: {e}")