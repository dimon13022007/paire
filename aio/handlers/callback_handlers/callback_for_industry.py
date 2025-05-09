from aiogram import Router, F
from aiogram.types import CallbackQuery
from aio.context.context_fsm import RegisterState
from aiogram.fsm.context import FSMContext
from text_translete.translate import get_translator
import gettext
from database.metod_for_database import MetodSQL
from aio.keyboards.keyboard_for_start import MetodKeyboardInline

router = Router(name=__name__)


@router.callback_query(F.data == "right")
async def right_part(callback: CallbackQuery):
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    text = _("Чем вы занимаетесь?")
    await callback.message.edit_reply_markup(text, reply_markup=await MetodKeyboardInline.industry_right())

@router.callback_query(F.data == "left")
async def right_part(callback: CallbackQuery):
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    text = _("Чем вы занимаетесь?")
    await callback.message.edit_reply_markup(text, reply_markup=await MetodKeyboardInline.industry_button())

@router.callback_query(lambda c: c.data in {
    "Backend", "Front-end", "FullStack", "GameDev", "MobileDev",
    "TelegramBots", "AI", "AppDev", "OSDev", "Cybersecurity",
    "Libraries", "Frameworks", "BlockchainDev"
})
async def industry_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer("")

    lang_param = await MetodSQL.get_language(callback_query.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    await state.update_data(industry=callback_query.data)
    await callback_query.answer(f"Ты выбрал {callback_query.data}")
    await state.set_state(RegisterState.img)
    text = _("Добавьте фото профиля📸")
    await callback_query.message.edit_text(text)




