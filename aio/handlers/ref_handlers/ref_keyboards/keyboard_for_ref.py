from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from text_translete.translate import get_translator
import gettext
from database.metod_for_database import MetodSQL


class RefKeyboards:

    @staticmethod
    async def ref_key(user_id: int):
        lang_param = await MetodSQL.get_language(user_id)
        print(lang_param)

        translator = await get_translator(lang_param)
        _ = translator.gettext

        refka = InlineKeyboardButton(text=_("Вернуться назад"), callback_data="back_ref")
        ref = InlineKeyboardMarkup(inline_keyboard=[[refka]])

        return ref


