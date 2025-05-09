from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram import F
from aio.handlers.routers.router_for_start import router
from database.metod_for_database import MetodSQL
from aio.keyboards.filter_keyboard.filter_keyboarad import FilterButton
from text_translete.translate import get_translator
import gettext

@router.message(Command("filter"))
async def filter_command(message: Message, state: FSMContext):
    lang_param = await MetodSQL.get_language(message.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    text = _("Выберите индустрию для фильтрации анкет:")
    await message.answer(text, reply_markup=await FilterButton.filter_industy(message.from_user.id))


@router.callback_query(F.data.startswith("set_filter_"))
async def set_filter_callback(callback: CallbackQuery, state: FSMContext):
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext
    industry = callback.data.split("_")[2]
    await state.update_data(industry_filter=industry)
    text = _("Фильтр установлен: {industry}.\nНажмите /show для поиска анкет.").format(industry=industry)
    await callback.message.edit_text(text)
    await callback.answer()


@router.callback_query(F.data == "filter_right")
async def right_part(callback: CallbackQuery):
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    text = _("Чем вы занимаетесь?")
    await callback.message.edit_reply_markup(text, reply_markup=await FilterButton.filter_right())

@router.callback_query(F.data == "filter_left")
async def left_part(callback: CallbackQuery):
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    text = _("Чем вы занимаетесь?")
    await callback.message.edit_reply_markup(text, reply_markup=await FilterButton.filter_industy(
        callback.from_user.id
    ))


@router.callback_query(F.data == "reset_filter")
async def reset_filter_callback(callback: CallbackQuery, state: FSMContext):
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext
    await state.update_data(industry_filter=None)
    text = _("Фильтр сброшен. Теперь ищем все анкеты  \n/show")
    await callback.message.answer(text)
    await callback.answer()
