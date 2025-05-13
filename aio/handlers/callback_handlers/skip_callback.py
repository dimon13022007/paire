from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aio.context.context_fsm import RegisterState
from aio.keyboards.keyboard_for_start import MetodKeyboardInline
from database.metod_for_database import MetodSQL
from text_translete.translate import get_translator
import gettext


router = Router()

@router.callback_query(F.data == "skip")
async def skip_param(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)

    data = await state.get_data()
    selected = data.get("language", [])

    translator = await get_translator(lang_param)
    _ = translator.gettext
    await state.update_data(text_disc=None)
    await state.set_state(RegisterState.language)
    text = _("Какой у вас язык программирования?")
    await callback.message.edit_text(text, reply_markup= await MetodKeyboardInline.language_button(selected))

