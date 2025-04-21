from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


ru_keyboard = InlineKeyboardButton(text="Russian", callback_data="ru")
en_keyboard = InlineKeyboardButton(text="English", callback_data="en")
uk_keyboard = InlineKeyboardButton(text="Ukrainian", callback_data="uk")
es_keyboard = InlineKeyboardButton(text="Spanish", callback_data="es")
de_keyboard = InlineKeyboardButton(text="German", callback_data="de")


row1 = [uk_keyboard,en_keyboard]
row2 = [ru_keyboard, es_keyboard, de_keyboard]

row = [row1, row2]

lang = InlineKeyboardMarkup(inline_keyboard=row)






