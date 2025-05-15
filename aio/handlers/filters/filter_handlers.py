from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from aio.handlers.routers.router_for_start import router
from database.metod_for_database import MetodSQL
from aio.keyboards.filter_keyboard.filter_keyboarad import FilterButton
from text_translete.translate import get_translator


async def get_or_init_fsm_list(state: FSMContext, key: str) -> list[str]:
    data = await state.get_data()
    value = data.get(key)
    if value is None:
        value = []
        await state.update_data({key: value})
    return value


@router.message(Command("filter"))
async def filter_command(message: Message, state: FSMContext):
    lang_param = await MetodSQL.get_language(message.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    data = await state.get_data()
    # selected = data.get("industries", [])

    selected = await get_or_init_fsm_list(state, "industries")

    text = _("Выберите индустрию для фильтрации анкет:")
    await message.answer(text, reply_markup=await FilterButton.filter_industy(message.from_user.id, selected))


@router.callback_query(F.data == "filter_next")
async def next(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    lang_param = await MetodSQL.get_language(callback.from_user.id)
    translator = await get_translator(lang_param)
    _ = translator.gettext

    data = await state.get_data()
    # selected = data.get("industries", [])

    selected = await get_or_init_fsm_list(state, "industries")

    if selected:
        industries_str = ",".join(selected)
        await MetodSQL.add_filter(callback.from_user.id, industries_str)
    else:
        await MetodSQL.delete_filter(callback.from_user.id)

    text = _("Фильтры сохранены: {industries}\nНажмите /show для просмотра анкет.").format(
        industries=", ".join(selected)
    )
    await callback.message.edit_text(text)


@router.callback_query(lambda c: c.data.startswith("set_filter_"))
async def toggle_filter_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    industry = callback.data.replace("set_filter_", "")

    lang_param = await MetodSQL.get_language(callback.from_user.id)
    translator = await get_translator(lang_param)
    _ = translator.gettext

    data = await state.get_data()
    # selected = data.get("industries", [])
    selected = await get_or_init_fsm_list(state, "industries")

    page = data.get("industry_page", "left")

    if industry in selected:
        selected.remove(industry)
    elif len(selected) < 9:
        selected.append(industry)
    else:
        await callback.answer(_("Можно выбрать не более 3 индустрий"), show_alert=True)
        return

    await state.update_data(industries=selected)

    text = _("Выберите индустрию для фильтрации анкет:")
    if page == "left":
        markup = await FilterButton.filter_industy(callback.from_user.id, selected)
    else:
        markup = await FilterButton.filter_right(selected)

    await callback.message.edit_text(text, reply_markup=markup)


@router.callback_query(F.data == "filter_right")
async def right_part(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(industry_page="right")

    lang_param = await MetodSQL.get_language(callback.from_user.id)
    translator = await get_translator(lang_param)
    _ = translator.gettext

    data = await state.get_data()
    # selected = data.get("industries", [])
    selected = await get_or_init_fsm_list(state, "industries")

    text = _("Выберите индустрию для фильтрации анкет:")
    markup = await FilterButton.filter_right(selected)
    await callback.message.edit_text(text, reply_markup=markup)


@router.callback_query(F.data == "filter_left")
async def left_part(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(industry_page="left")

    lang_param = await MetodSQL.get_language(callback.from_user.id)
    translator = await get_translator(lang_param)
    _ = translator.gettext

    data = await state.get_data()
    # selected = data.get("industries", [])
    selected = await get_or_init_fsm_list(state, "industries")

    text = _("Выберите индустрию для фильтрации анкет:")
    markup = await FilterButton.filter_industy(callback.from_user.id, selected)
    await callback.message.edit_text(text, reply_markup=markup)



@router.callback_query(F.data == "reset_filter")
async def reset_filter_callback(callback: CallbackQuery):
    await callback.answer()

    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext
    await MetodSQL.delete_filter(callback.from_user.id)
    text = _("Фильтр сброшен. Теперь ищем все анкеты  \n/show")
    await callback.message.answer(text)
    await callback.answer()
