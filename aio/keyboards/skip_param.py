from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from database.metod_for_database import MetodSQL
from text_translete.translate import get_translator
import gettext


class SkipButton:
    @staticmethod
    async def skip(user_id):
        lang_param = await MetodSQL.get_language(user_id)
        print(lang_param)

        translator = await get_translator(lang_param)
        _ = translator.gettext

        skip = InlineKeyboardButton(text=_("Пропустить"), callback_data="skip")

        skip_param = InlineKeyboardMarkup(inline_keyboard=[[skip]])
        return skip_param
