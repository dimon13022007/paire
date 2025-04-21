from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.metod_for_database import MetodSQL
from text_translete.translate import get_translator
from database.metod_for_database import MetodSQL
from text_translete.translate import get_translator
import gettext

class RefCode:

    @staticmethod
    async def refka(user_id):

        lang_param = await MetodSQL.get_language(user_id)
        translator = await get_translator(lang_param)
        _ = translator.gettext

        code = InlineKeyboardButton(text=_("Получить код"), callback_data="code")
        refka = InlineKeyboardButton(text=_("Использовать код"), callback_data="code2")


        ref_code = InlineKeyboardMarkup(inline_keyboard=[[code, refka]])
        return ref_code

    @staticmethod
    async def refka_back(user_id):

        lang_param = await MetodSQL.get_language(user_id)
        translator = await get_translator(lang_param)
        _ = translator.gettext

        code = InlineKeyboardButton(text=_("Получить код"), callback_data="code")
        refka = InlineKeyboardButton(text=_("Использовать код"), callback_data="code2")
        back = InlineKeyboardButton(text=_("Назад 🔙"), callback_data="back_refka")

        row = [back]
        rows = [code, refka]
        ro = [rows, row]
        ref_code = InlineKeyboardMarkup(inline_keyboard=ro)
        return ref_code

