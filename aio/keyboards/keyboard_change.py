from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.metod_for_database import MetodSQL
from text_translete.translate import get_translator



class ChangeAnketa:

    @staticmethod
    async def changed_register(user_id):
        lang_param = await MetodSQL.get_language(user_id)
        translator = await get_translator(lang_param)
        _ = translator.gettext

        change0 = InlineKeyboardButton(text=_("Город 🌇"), callback_data="change_city")
        change1 = InlineKeyboardButton(text=_("Имя 📝"), callback_data="change_name")
        change2 = InlineKeyboardButton(text=_("Возраст 🎂"), callback_data="change_age")
        change3 = InlineKeyboardButton(text=_("Описание 🗒️"), callback_data="change_text_disc")
        change5 = InlineKeyboardButton(text=_("Язык 🌐"), callback_data="change_lang")
        change6 = InlineKeyboardButton(text=_("Отрасль 🏭"), callback_data="change_industry")
        change7 = InlineKeyboardButton(text=_("Фото 📸"), callback_data="change_img")
        change = InlineKeyboardButton(text=_("Назад"), callback_data="che_img")

        row = [change0, change1]
        row2 = [change2,change3]
        row3 = [change5, change6]
        row4 = [change7]
        main_row = [row, row2, row3, row4]
        chande_anketa = InlineKeyboardMarkup(inline_keyboard=main_row)
        return chande_anketa










