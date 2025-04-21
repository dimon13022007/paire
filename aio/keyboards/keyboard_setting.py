from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.metod_for_database import MetodSQL
from text_translete.translate import get_translator
import gettext



class SettingButton:

    @staticmethod
    async def setting_button(user_id):
        lang_param = await MetodSQL.get_language(user_id)
        translator = await get_translator(lang_param)
        _ = translator.gettext

        my_profile = InlineKeyboardButton(text=_("Мой профиль 👤"), callback_data="my_prof")
        filter = InlineKeyboardButton(text=_("Фильтры 🔎"), callback_data="filter")
        deactivate = InlineKeyboardButton(text=_("Деактивировать анкету 🛑"), callback_data="deactivate_anketa")
        ref_code = InlineKeyboardButton(text=_("Реферальный код 🎁"), callback_data="refcode")
        language_change = InlineKeyboardButton(text=_("Изменить язык 🌏"), callback_data="language_lang")
        back = InlineKeyboardButton(text=_("Назад 🔙"), callback_data="back_main_menu")


        _ = translator.gettext
        row1 = [my_profile, filter]
        row2 = [ref_code, language_change]
        row3 = [deactivate]
        row4 = [back]
        main_row = [row1, row2, row3, row4]

        chande_register = InlineKeyboardMarkup(inline_keyboard=main_row)
        return chande_register