# PairCode/admin_panel/for_admin_ad.py

import os
import logging
from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from database.models import Advertisement
from aio.bot_token import bot
from database.engine import async_sessions
from aio.context.context_new_ad import AdInputState

router = Router()
ADMIN_IDS = [826039504, 6091410541]

logger = logging.getLogger(__name__)

@router.message(Command("admin_ad_158"))
async def start_ad_input(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ У тебя нет доступа к этой команде.")
        return

    await message.answer("✏️ Введи текст новой рекламы:")
    await state.set_state(AdInputState.text)


@router.message(AdInputState.text)
async def receive_ad_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer("📎 Теперь отправь картинку или нажми /skip_ad_image, если без неё")
    await state.set_state(AdInputState.image)


@router.message(AdInputState.image, F.photo)
async def receive_ad_image(message: Message, state: FSMContext):
    photo = message.photo[-1]
    file_path = f"media/ad_{photo.file_unique_id}.jpg"
    os.makedirs("media", exist_ok=True)

    file = await bot.get_file(photo.file_id)
    await bot.download_file(file.file_path, destination=file_path)

    data = await state.get_data()
    ad_text = data.get("text", "Без текста")

    async with async_sessions() as session:
        ad = Advertisement(text=ad_text, image_path=file_path)
        session.add(ad)
        await session.commit()

    await state.clear()
    await message.answer("✅ Реклама с изображением сохранена!")


@router.message(AdInputState.image, Command("skip_ad_image"))
async def skip_image(message: Message, state: FSMContext):
    data = await state.get_data()

    async with async_sessions() as session:
        ad = Advertisement(text=data['text'], image_path=None)
        session.add(ad)
        await session.commit()

    await message.answer("✅ Реклама без картинки сохранена!")
    await state.clear()


@router.message(AdInputState.image)
async def not_photo(message: Message):
    await message.answer("⛔ Пожалуйста, отправь именно изображение или нажми /skip_ad_image")
