from aiogram.types import CallbackQuery, Message
from .translate import get_translator
from database.metod_for_database import MetodSQL


async def send_translated_message(user_id: int, message_or_callback, text: str, reply_markup=None):
    user_lang = await MetodSQL.get_language(user_id)
    print(user_lang)

    _ = await get_translator(user_lang)
    translated_text = _.gettext(text)

    if isinstance(message_or_callback, CallbackQuery):
        if reply_markup is None:
            await message_or_callback.message.answer(translated_text)
        else:
            await message_or_callback.message.answer(translated_text, reply_markup=reply_markup)

    elif isinstance(message_or_callback, Message):
        if reply_markup is None:
            await message_or_callback.answer(translated_text)
        else:
            await message_or_callback.answer(translated_text, reply_markup=reply_markup)
