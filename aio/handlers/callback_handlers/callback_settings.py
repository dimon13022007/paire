from aiogram.types import CallbackQuery
from aiogram import Router,F
from database.metod_for_database import MetodSQL
from text_translete.translate import get_translator
from aio.keyboards.keyboard_setting import SettingButton

router = Router()

@router.callback_query(F.data == "settings")
async def setting_handler(callback: CallbackQuery):
    await callback.answer("")

    user_id = callback.from_user.id

    lang_param = await MetodSQL.get_language(user_id)
    translator = await get_translator(lang_param)
    _ = translator.gettext

    text = _("Настройки:")
    await callback.message.answer(text, reply_markup=await SettingButton.setting_button(user_id))





