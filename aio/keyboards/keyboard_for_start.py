from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.metod_for_database import MetodSQL
from text_translete.translate import get_translator
import gettext



en_keyboard = InlineKeyboardButton(text="🇬🇧", callback_data="en")
es_keyboard = InlineKeyboardButton(text="🇪🇸", callback_data="es")
de_keyboard = InlineKeyboardButton(text="🇩🇪", callback_data="de")
uk_keyboard = InlineKeyboardButton(text="🇺🇦", callback_data="uk")
ru_keyboard = InlineKeyboardButton(text="🇷🇺", callback_data="ru")
kk_keyboard = InlineKeyboardButton(text="🇰🇿", callback_data="kk")



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



class MetodKeyboardInline:


    @staticmethod
    async def language_commnad():
        row1 = [uk_keyboard, en_keyboard]
        row2 = [es_keyboard, de_keyboard]
        row3 = [ru_keyboard, kk_keyboard]
        row = [row1, row2, row3]
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
        row4 = [back_lang]
        row = [row1, row2, row3, row4]
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
    async def language_button(user_id: int):
        lang_param = await MetodSQL.get_language(user_id)
        print(lang_param)

        translator = await get_translator(lang_param)
        _ = translator.gettext
        another_keyboard = InlineKeyboardButton(text=_("Другое"), callback_data="Другое")

        rows_first = [python_keyboard, java_keyboard]
        row_second = [java_script_keyboard, php_keyboard]
        row_third = [go_keyboard, c_keyboard]
        row_4 = [csharp_keyboard, swift_keyboard]
        row_5 = [kotlin_keyboard, r_keyboard]
        row_6 = [another_keyboard]

        row = [rows_first, row_second, row_third, row_4, row_5, row_6]

        language = InlineKeyboardMarkup(inline_keyboard=row
        )
        return language

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
    async def industry_button():
        row_1 = [backend, frontend, fullstack]
        row_2 = [gamedev,mobiledev]
        row = [row_1, row_2]
        industry = InlineKeyboardMarkup(inline_keyboard=row)
        return industry

