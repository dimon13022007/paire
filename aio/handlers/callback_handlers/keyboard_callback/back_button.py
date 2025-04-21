from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.metod_for_database import MetodSQL
from text_translete.translate import get_translator



class BackButton:


    @staticmethod
    async def back_button(user_id):
        lang_param = await MetodSQL.get_language(user_id)
        translator = await get_translator(lang_param)
        _ = translator.gettext

        back_button = InlineKeyboardButton(text=_("Назад 🔙"), callback_data="back_to_setting")

        _ = translator.gettext
        row = [back_button]

        main_row = [row]
        back = InlineKeyboardMarkup(inline_keyboard=main_row)
        return back




