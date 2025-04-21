from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aio.bot_token import bot
from aio.handlers.routers.router_for_start import router
from aio.keyboards.keyboard_for_restart_register import ChangeRegister
from aio.func.func_profile import profile
from database.metod_for_database import MetodSQL
import logging
from text_translete.translate import get_translator
import gettext

logger = logging.getLogger(__name__)

@router.message(Command("show"))
async def show_profiles_command(message: Message, state: FSMContext):
    lang_param = await MetodSQL.get_language(message.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext
    user_id = message.from_user.id

    try:
        prof = profile(bot, user_id, message.chat.id, reply_mark=await ChangeRegister.changed_register(message.from_user.id))
        if not prof:
            text = _("У вас пока что нету анкеты")
            await message.answer(text)
        else:
            await prof
    except Exception as e:
        logger.error(f"Ошибка при получении профиля для пользователя {user_id}: {e}")
        text = _("Произошла ошибка при загрузке профиля. Попробуйте снова позже.")
        await message.answer(text)
