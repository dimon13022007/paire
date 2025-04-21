from aiogram import Router
from aiogram.filters.command import Command, Message
from aio.keyboards.keyboard_for_start import MetodKeyboardInline
from text_translete.translate import get_translator
import gettext
from database.metod_for_database import MetodSQL
from aiogram.types import CallbackQuery

router = Router()

@router.message(Command("language"))
async def language(message: Message):
    lang_param = await MetodSQL.get_language(message.from_user.id)

    translator = await get_translator(lang_param)
    _ = translator.gettext
    text = _("На каком языке вы хотели бы объединяться с другими ИТ-специалистами? 🌍")
    await message.answer(
        text,
        reply_markup=await MetodKeyboardInline.language_commnad()
    )


@router.callback_query(lambda c: c.data in {
    "en", "es", "de",
    "uk", "ru",
    "kk"
})
async def update_language(callback: CallbackQuery):
    lang_param = await MetodSQL.get_language(callback.from_user.id)

    translator = await get_translator(lang_param)
    _ = translator.gettext
    await MetodSQL.update_lang(callback.from_user.id, callback.data)
    text = _("Язык обновлен")
    await callback.message.answer(text)





