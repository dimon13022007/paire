from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.metod_for_database import MetodSQL
from text_translete.translate import get_translator



en_keyboard = InlineKeyboardButton(text="🇬🇧", callback_data="en")
es_keyboard = InlineKeyboardButton(text="🇪🇸", callback_data="es")
de_keyboard = InlineKeyboardButton(text="🇩🇪", callback_data="de")
uk_keyboard = InlineKeyboardButton(text="🇺🇦", callback_data="uk")
ru_keyboard = InlineKeyboardButton(text="🇷🇺", callback_data="ru")
kk_keyboard = InlineKeyboardButton(text="🇰🇿", callback_data="kk")
ky_keyboard = InlineKeyboardButton(text="🇰🇬", callback_data="ky")
it_keyboard = InlineKeyboardButton(text="🇮🇹", callback_data="it")




python_keyboard = InlineKeyboardButton(text="Python", callback_data="Python")
java_keyboard = InlineKeyboardButton(text="Java", callback_data="Java")
java_script_keyboard = InlineKeyboardButton(text="JavaScript", callback_data="JavaScript")
php_keyboard = InlineKeyboardButton(text="PHP", callback_data="PHP")
go_keyboard = InlineKeyboardButton(text="Go", callback_data="Go")
c_keyboard = InlineKeyboardButton(text="C,C++", callback_data="C,C++")
csharp_keyboard = InlineKeyboardButton(text="C#", callback_data="C#")
swift_keyboard = InlineKeyboardButton(text="Swift", callback_data="Swift")
kotlin_keyboard = InlineKeyboardButton(text="Kotlin", callback_data="Kotlin")
r_keyboard = InlineKeyboardButton(text="R", callback_data="R")

backend = InlineKeyboardButton(text="Backend", callback_data="Backend")
frontend = InlineKeyboardButton(text="Front-end", callback_data="Front-end")
fullstack = InlineKeyboardButton(text="Full Stack", callback_data="FullStack")
gamedev = InlineKeyboardButton(text="GameDev", callback_data="GameDev")
mobiledev = InlineKeyboardButton(text="MobileDev", callback_data="MobileDev")
telegram_bots = InlineKeyboardButton(text=" Telegram Bots", callback_data="TelegramBots")
ai = InlineKeyboardButton(text=" AIDev", callback_data="AI")
app_dev = InlineKeyboardButton(text=" AppDev", callback_data="AppDev")
os_dev = InlineKeyboardButton(text=" OSDev", callback_data="OSDev")
cybersec = InlineKeyboardButton(text=" Cybersecurity", callback_data="Cybersecurity")
libraries = InlineKeyboardButton(text=" Libraries", callback_data="Libraries")
blockchain = InlineKeyboardButton(text=" BlockchainDev", callback_data="BlockchainDev")
right = InlineKeyboardButton(text="➡️", callback_data="right")
left = InlineKeyboardButton(text="⬅️", callback_data="left")
nice = InlineKeyboardButton(text="Готово▶️", callback_data="nice")


class MetodKeyboardInline:


    @staticmethod
    async def language_commnad():
        row1 = [uk_keyboard, en_keyboard]
        row2 = [es_keyboard, de_keyboard]
        row3 = [ru_keyboard, kk_keyboard]
        row4 = [ky_keyboard, it_keyboard]
        row = [row1, row2, row3, row4]
        lang = InlineKeyboardMarkup(inline_keyboard=row)
        return lang

    @staticmethod
    async def lang_back(user_id):
        lang_param = await MetodSQL.get_language(user_id)
        translator = await get_translator(lang_param)
        _ = translator.gettext

        back_lang = InlineKeyboardButton(text=_("Назад 🔙"), callback_data="back_lang")

        row1 = [uk_keyboard, en_keyboard]
        row2 = [es_keyboard, de_keyboard]
        row3 = [ru_keyboard, kk_keyboard]
        row_3 = [ky_keyboard,it_keyboard]
        row4 = [back_lang]
        row = [row1, row2, row3,row_3, row4]
        lang = InlineKeyboardMarkup(inline_keyboard=row)
        return lang



    @staticmethod
    async def start_command(user_id: int):
        lang_param = await MetodSQL.get_language(user_id)
        translator = await get_translator(lang_param)
        _ = translator.gettext

        start_keyboard = InlineKeyboardButton(text=_("Начать регистрацию "), callback_data="city")
        start = InlineKeyboardMarkup(inline_keyboard=[[start_keyboard]])
        return start

    @staticmethod
    async def language_button(user_id,selected: list[str]):
        lang_param = await MetodSQL.get_language(user_id)
        translator = await get_translator(lang_param)
        _ = translator.gettext

        def mark(name: str) -> InlineKeyboardButton:
            text = f"{name} ✅" if name in selected else name
            return InlineKeyboardButton(text=text, callback_data=name)

        row_1 = [mark("Python"), mark("Java")]
        row_2 = [mark("JavaScript"), mark("PHP")]
        row_3 = [mark("Go"), mark("C,C++")]
        row_4 = [mark("C#"), mark("Swift")]
        row_5 = [mark("Kotlin"), mark("R")]
        row_6 = [InlineKeyboardButton(text=_("Готово▶️"), callback_data="success")]

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            row_1, row_2, row_3, row_4, row_5,row_6
        ])
        return keyboard

    @staticmethod
    async def another_button(user_id: int):
        lang_param = await MetodSQL.get_language(user_id)
        translator = await get_translator(lang_param)
        _ = translator.gettext

        yes = InlineKeyboardButton(text=_("Да"), callback_data="Yes")
        no = InlineKeyboardButton(text=_("Помянять"), callback_data="change")

        row1 = [yes, no]
        row = [row1]
        another = InlineKeyboardMarkup(inline_keyboard=row)
        return another

    @staticmethod
    async def industry_button(user_id,selected: list[str]):
        lang_param = await MetodSQL.get_language(user_id)
        translator = await get_translator(lang_param)
        _ = translator.gettext
        def mark(name: str) -> InlineKeyboardButton:
            text = f"{name} ✅" if name in selected else name
            return InlineKeyboardButton(text=text, callback_data=name)

        row_1 = [mark("Backend"), mark("Front-end")]
        row_2 = [mark("FullStack"), mark("MobileDev")]
        row_4 = [InlineKeyboardButton(text="➡️", callback_data="right")]
        row_5 = [InlineKeyboardButton(text=_("Готово▶️"), callback_data="nice")]

        return InlineKeyboardMarkup(inline_keyboard=[row_1, row_2, row_4, row_5])

    @staticmethod
    async def industry_right(selected: list[str]):
        def mark(name: str) -> InlineKeyboardButton:
            text = f"{name} ✅" if name in selected else name
            return InlineKeyboardButton(text=text, callback_data=name)

        row_1 = [mark("Cybersecurity"), mark("Libraries")]
        row_2 = [mark("BlockchainDev"), mark("AppDev")]
        row_3 = [mark("AI"), mark("OSDev")]
        row_3_0 = [mark("GameDev"), mark("TelegramBots")]
        row_4 = [InlineKeyboardButton(text="⬅️", callback_data="left")]
        row_5 = [InlineKeyboardButton(text="▶️", callback_data="nice")]


        return InlineKeyboardMarkup(inline_keyboard=[row_1, row_2,row_3_0, row_3, row_4, row_5])

