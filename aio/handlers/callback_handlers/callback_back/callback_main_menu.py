from aiogram.types import CallbackQuery
from aiogram import Router, F
from aio.keyboards.keyboard_for_restart_register import ChangeRegister
from database.metod_for_database import MetodSQL
from text_translete.translate import get_translator
from aio.func.func_profile import profile
from aio.bot_token import bot
from aio.keyboards.keyboard_setting import SettingButton

router = Router()


@router.callback_query(F.data == "back_main_menu")
async def back_main(callback: CallbackQuery):
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    translator = await get_translator(lang_param)
    _ = translator.gettext

    await callback.answer("")
    user_id = callback.from_user.id
    user = int(user_id)

    await callback.message.delete()


    # await profile(bot,user, callback.message.chat.id, reply_mark=await ChangeRegister.changed_register(callback.from_user.id))


@router.callback_query(F.data == "back_setting_menu")
async def setting_menu(callback: CallbackQuery):
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    translator = await get_translator(lang_param)
    _ = translator.gettext

    await callback.answer("")
    await callback.message.delete()

    text = _("Настройки:")
    await callback.message.answer(text, reply_markup=await SettingButton.setting_button(callback.from_user.id))


@router.callback_query(F.data == "back_refka")
async def refka_menu(callback: CallbackQuery):
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    translator = await get_translator(lang_param)
    _ = translator.gettext

    await callback.answer("")
    await callback.message.delete()

    text = _("Настройки:")
    await callback.message.answer(text, reply_markup=await SettingButton.setting_button(callback.from_user.id))

@router.callback_query(F.data == "back_lang")
async def back_lang(callback: CallbackQuery):
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    translator = await get_translator(lang_param)
    _ = translator.gettext

    await callback.answer("")
    await callback.message.delete()

    text = _("Настройки:")
    await callback.message.answer(text, reply_markup=await SettingButton.setting_button(callback.from_user.id))




