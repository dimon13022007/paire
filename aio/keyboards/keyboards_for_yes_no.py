from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from database.metod_for_database import MetodSQL
from text_translete.translate import get_translator

class KeyBoardYesNo:

    @staticmethod
    async def yes_no(user_id):
        lang_param = await MetodSQL.get_language(user_id)
        translator = await get_translator(lang_param)
        _ = translator.gettext

        yes = InlineKeyboardButton(text=_("️Да"), callback_data="yes_industry")
        net = InlineKeyboardButton(text=_("Нет"), callback_data="no_industry")

        _ = translator.gettext
        row = [yes, net]
        main_row = [row]
        chande_register = InlineKeyboardMarkup(inline_keyboard=main_row)
        return chande_register







