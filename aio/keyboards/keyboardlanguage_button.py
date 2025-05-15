from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


ru_keyboard = InlineKeyboardButton(text="Russian", callback_data="ru")
en_keyboard = InlineKeyboardButton(text="English", callback_data="en")
uk_keyboard = InlineKeyboardButton(text="Ukrainian", callback_data="uk")
es_keyboard = InlineKeyboardButton(text="Spanish", callback_data="es")
de_keyboard = InlineKeyboardButton(text="German", callback_data="de")
ky_keyboard = InlineKeyboardButton(text="Kyrgyz", callback_data="ky")
it_keyboard = InlineKeyboardButton(text="Italian", callback_data="it")

row1 = [uk_keyboard,en_keyboard]
row2 = [ru_keyboard, es_keyboard, de_keyboard]
row_3 = [ky_keyboard,it_keyboard]
row = [row1, row2, row_3]

lang = InlineKeyboardMarkup(inline_keyboard=row)






