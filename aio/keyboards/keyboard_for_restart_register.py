from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from database.metod_for_database import MetodSQL
from text_translete.translate import get_translator



class ChangeRegister:


    @staticmethod
    async def changed_register(user_id):
        lang_param = await MetodSQL.get_language(user_id)
        translator = await get_translator(lang_param)
        _ = translator.gettext

        search = InlineKeyboardButton(text=_("Поиск 🕵️"), callback_data="search")
        change = InlineKeyboardButton(text=_("Новая анкета 📝"), callback_data="change_anketa")
        change_param = InlineKeyboardButton(text=_("Изменить параметры 🛠"), callback_data="change_param")
        settings = InlineKeyboardButton(text=_("Настройки 🔧"), callback_data="settings")

        _ = translator.gettext
        row = [search,change]
        row2 = [change_param]
        row3= [settings]
        main_row = [row, row2, row3]
        chande_register = InlineKeyboardMarkup(inline_keyboard=main_row)
        return chande_register

    @staticmethod
    async def location_change():
        ...