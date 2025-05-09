from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from text_translete.translate import get_translator
from database.metod_for_database import MetodSQL
import gettext

backend = InlineKeyboardButton(text="Backend", callback_data="set_filter_Backend")
frontend = InlineKeyboardButton(text="Front-end", callback_data="set_filter_Front-end")
fullstack = InlineKeyboardButton(text="Full Stack", callback_data="set_filter_Full Stack")
gamedev = InlineKeyboardButton(text="GameDev", callback_data="set_filter_GameDev")
mobiledev = InlineKeyboardButton(text="MobileDev", callback_data="set_filter_MobileDev")
telegram_bots = InlineKeyboardButton(text=" Telegram Bots", callback_data="selt_filter_Telegram Bots")
ai = InlineKeyboardButton(text=" AIDev", callback_data="set_filter_AIDev")
app_dev = InlineKeyboardButton(text=" AppDev", callback_data="set_filter_AppDev")
os_dev = InlineKeyboardButton(text=" OSDev", callback_data="set_filter_OSDev")
cybersec = InlineKeyboardButton(text=" Cybersecurity", callback_data="set_filter_Cybersecurity")
libraries = InlineKeyboardButton(text=" Libraries", callback_data="set_filter_Libraries")
blockchain = InlineKeyboardButton(text=" BlockchainDev", callback_data="set_filter_BlockchainDev")
right = InlineKeyboardButton(text="➡️", callback_data="filter_right")
left = InlineKeyboardButton(text="⬅️", callback_data="filter_left")

class FilterButton:

    @staticmethod
    async def filter_industy(user_id):
        lang_param = await MetodSQL.get_language(user_id)
        translator = await get_translator(lang_param)
        _ = translator.gettext
        set_filter = InlineKeyboardButton(text=_("Скинуть фильтры"), callback_data="reset_filter")

        row_1 = [backend, frontend]
        row_2 = [fullstack,mobiledev]
        row_3 = [gamedev, telegram_bots]
        row_4 = [right]
        row_5 = [set_filter]
        row = [row_1, row_2, row_3, row_5, row_4]

        industry = InlineKeyboardMarkup(inline_keyboard=row)
        return industry

    @staticmethod
    async def filter_right():
        row_1 = [cybersec, libraries]
        row_2 = [blockchain, app_dev]
        row_3 = [ai, os_dev]
        row_4 = [left]
        row = [row_1, row_2,row_3, row_4]

        industry = InlineKeyboardMarkup(inline_keyboard=row)
        return industry












