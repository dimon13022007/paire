import asyncio
import time

from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from aio.handlers.routers.router_for_start import router
from aio.state.session_memory import disliked_users
from aio.services.match_service import proceed_to_next_profile, logger
from database.metod_for_database import MetodSQL
from text_translete.translate import get_translator
import gettext
from datetime import datetime


user_last_click = {}


@router.callback_query(F.data.startswith("dislike_"))
async def dislike_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    now = time.time()

    if (last_click := user_last_click.get(user_id)) and now - last_click < 1:
        await callback.answer("⏳ Подождите немного...", show_alert=False)
        return
    user_last_click[user_id] = now

    await callback.answer()

    disliked_id = int(callback.data.split("_")[1])
    disliked_users.setdefault(user_id, set()).add(disliked_id)

    try:
        await callback.message.delete()
    except Exception as e:
        logger.warning(f"Не удалось удалить сообщение: {e}")

    await asyncio.shield(proceed_to_next_profile(state, callback))
