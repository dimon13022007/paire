from database.metod_for_database import MetodSQL

from functools import wraps
from aiogram.types import CallbackQuery, Message
from text_translete.translate import get_translator
import gettext


def check_registration():
    def decorator(func):
        @wraps(func)
        async def wrapper(event: CallbackQuery | Message, *args, **kwargs):
            user_id = event.from_user.id
            is_registered = await MetodSQL.prim_key(user_id)

            lang_param = await MetodSQL.get_language(user_id)
            print(lang_param)

            translator = await get_translator(lang_param)
            _ = translator.gettext

            if is_registered:
                return await func(event, *args, **kwargs)
            else:
                text = _("Вы не зарегистрированы. Пожалуйста, зарегистрируйтесь перед использованием, введите команду /start")
                await event.answer(text)

        return wrapper

    return decorator



