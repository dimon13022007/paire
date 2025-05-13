from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from text_translete.translate import get_translator
from database.metod_for_database import MetodSQL

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
    async def filter_industy(user_id, selected: list[str]):
        lang_param = await MetodSQL.get_language(user_id)
        translator = await get_translator(lang_param)
        _ = translator.gettext

        def mark(name: str) -> InlineKeyboardButton:
            text = f"{name} ✅" if name in selected else name
            return InlineKeyboardButton(text=text, callback_data=f"set_filter_{name}")

        set_filter = InlineKeyboardButton(text="🔄 Сброс", callback_data="reset_filter")
        success = InlineKeyboardButton(text="✅ Готово", callback_data="filter_next")
        right = InlineKeyboardButton(text="➡️", callback_data="filter_right")


        row_1 = [mark("Backend"), mark("Front-end")]
        row_2 = [mark("Full Stack"), mark("MobileDev")]
        row_3 = [mark("GameDev"), mark("Telegram Bots")]
        row_4 = [set_filter]
        row_5 = [success]
        row_6 = [right]

        keyboard = InlineKeyboardMarkup(inline_keyboard=[row_1, row_2, row_3,row_4, row_6, row_5])
        return keyboard

    @staticmethod
    async def filter_right(selected: list[str]):
        def mark(name: str) -> InlineKeyboardButton:
            text = f"{name} ✅" if name in selected else name
            return InlineKeyboardButton(text=text, callback_data=f"set_filter_{name}")

        left = InlineKeyboardButton(text="⬅️", callback_data="filter_left")

        row_1 = [mark("Cybersecurity"), mark("Libraries")]
        row_2 = [mark("BlockchainDev"), mark("AppDev")]
        row_3 = [mark("AIDev"), mark("OSDev")]
        row_4 = [left]

        keyboard = InlineKeyboardMarkup(inline_keyboard=[row_1, row_2, row_3, row_4])
        return keyboard











