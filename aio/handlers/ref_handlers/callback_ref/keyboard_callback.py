from aiogram.types import CallbackQuery
from aiogram import Router, F
from aiogram import Router
from aio.keyboards.keyboard_ref import RefCode
from database.metod_for_database import MetodSQL
from text_translete.translate import get_translator
import gettext

router = Router()

@router.callback_query(F.data == "back_ref")
async def ref_callback(callback: CallbackQuery):
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext
    text = _("👋 Здравствуйте!\n\n"
        "Здесь вы можете получить свой реферальный код. "
        "Передайте его другу, чтобы он смог указать ваш код при регистрации. "
        "В результате вы получите буст анкеты! 🚀")
    await callback.message.edit_text(
        text
    ,reply_markup=await RefCode.refka(callback.from_user.id))








