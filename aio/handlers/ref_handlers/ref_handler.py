from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from aio.keyboards.keyboard_ref import RefCode
from .admin_panel.admin import check_registration
from database.metod_for_database import MetodSQL
from text_translete.translate import get_translator
import gettext

router = Router()

@router.message(Command("ref"))
@check_registration()
async def ref_command(message: Message):
    lang_param = await MetodSQL.get_language(message.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext
    text = _("👋 Здравствуйте!\n\n"
        "Здесь вы можете получить свой реферальный код. "
        "Передайте его другу, чтобы он смог указать ваш код при регистрации. "
        "В результате вы получите буст анкеты! 🚀")
    await message.answer(
        text
    ,reply_markup=await RefCode.refka(message.from_user.id))

