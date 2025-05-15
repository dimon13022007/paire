from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from aio.context.context_fsm import RegisterState
from text_translete.translate import get_translator
import gettext
from database.metod_for_database import MetodSQL
from aio.keyboards.keyboard_for_start import MetodKeyboardInline

router = Router(name=__name__)


@router.callback_query(F.data == "right")
async def right_part(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await state.update_data(industry_page="right")

    lang_param = await MetodSQL.get_language(callback.from_user.id)
    translator = await get_translator(lang_param)
    _ = translator.gettext

    data = await state.get_data()
    selected = data.get("industries", [])

    markup = await MetodKeyboardInline.industry_right(selected)
    await callback.message.edit_reply_markup(reply_markup=markup)


@router.callback_query(F.data == "left")
async def left_part(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(industry_page="left")

    lang_param = await MetodSQL.get_language(callback.from_user.id)
    translator = await get_translator(lang_param)
    _ = translator.gettext

    data = await state.get_data()
    selected = data.get("industries", [])

    markup = await MetodKeyboardInline.industry_button(callback.from_user.id,selected)
    await callback.message.edit_reply_markup(reply_markup=markup)


@router.callback_query(lambda c: c.data in {
    "Backend", "Front-end", "FullStack", "GameDev", "MobileDev",
    "TelegramBots", "AI", "AppDev", "OSDev", "Cybersecurity",
    "Libraries", "Frameworks", "BlockchainDev"
})
async def industry_callback(callback_query: CallbackQuery, state: FSMContext):
    lang_param = await MetodSQL.get_language(callback_query.from_user.id)
    translator = await get_translator(lang_param)
    _ = translator.gettext

    data = await state.get_data()
    selected = data.get("industries", [])
    page = data.get("industry_page", "left")

    industry = callback_query.data

    if industry in selected:
        selected.remove(industry)
    elif len(selected) < 3:
        selected.append(industry)
    else:
        text = _("Максимум 3")
        await callback_query.answer(text)
        return

    await state.update_data(industries=selected)

    text = _("Выберите индустрии, повторное нажатие снимает выбор:")
    if page == "left":
        markup = await MetodKeyboardInline.industry_button(callback_query.from_user.id,selected)
    else:
        markup = await MetodKeyboardInline.industry_right(selected)

    await callback_query.message.edit_text(text, reply_markup=markup)


@router.callback_query(F.data == "nice")
async def nice_callback(callback: CallbackQuery, state: FSMContext):
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    translator = await get_translator(lang_param)
    _ = translator.gettext
    data = await state.get_data()

    selected = data.get("industries", [])

    if not selected:
        await callback.answer("Выберите хотя бы одну индустрию")
        return
    text = _("Добавьте фото профиля📸")
    await callback.message.edit_text(text)
    await state.set_state(RegisterState.img)



