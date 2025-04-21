from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from database.metod_for_database import MetodSQL
from aio.bot_token import bot
from aio.func.func_profile import profile
from aio.keyboards.keyboard_for_restart_register import ChangeRegister
from aio.handlers.routers.router_for_start import router
import logging
from text_translete.translate import get_translator
import gettext

logger = logging.getLogger(__name__)

@router.callback_query(F.data == "show_profile")
async def show_profile_callback(callback: CallbackQuery, state: FSMContext):
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    user_id = callback.from_user.id
    try:
        await callback.message.answer("💤")
        await callback.message.edit_reply_markup(reply_markup=None)
        await profile(bot, user_id, callback.message.chat.id, reply_mark=await ChangeRegister.changed_register(callback.from_user.id))
    except Exception as e:
        logger.error(f"Ошибка при получении профиля {user_id}: {e}")
        text = _("Произошла ошибка при загрузке профиля.")
        await callback.message.answer(text)
