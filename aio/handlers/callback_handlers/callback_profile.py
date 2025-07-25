from aiogram import Router
from aio.func.func_profile import profile
from aio.bot_token import bot
from aio.keyboards.keyboard_for_restart_register import ChangeRegister
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from database.metod_for_database import MetodSQL
from text_translete.translate import get_translator
from aio.keyboards.keyboard_ref import RefCode
from aio.keyboards.keyboard_for_start import MetodKeyboardInline
from aio.keyboards.filter_keyboard.filter_keyboarad import FilterButton
from aio.handlers.filters.filter_handlers import get_or_init_fsm_list

router = Router()


@router.callback_query(F.data == "my_prof")
async def profile_handler(callback: CallbackQuery):
    await callback.answer("")

    user_id = callback.from_user.id

    lang_param = await MetodSQL.get_language(user_id)
    translator = await get_translator(lang_param)
    _ = translator.gettext

    try:
        prof = profile(bot, user_id, callback.message.chat.id, reply_mark=await ChangeRegister.changed_register(callback.from_user.id))
        if not prof:
            text = _("У вас покачто нету анкеты")
            await callback.message.edit_text(text)
        else:
            await prof
    except Exception:
        text = _("Произошла ошибка при загрузке профиля. Попробуйте снова позже.")
        await callback.message.answer(text)


@router.callback_query(F.data == "filter")
async def filter_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")

    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)

    data = await state.get_data()
    # selected = data.get("language", [])
    selected = await get_or_init_fsm_list(state, "industries")

    translator = await get_translator(lang_param)
    _ = translator.gettext
    text = _("Выберите индустрию для фильтрации анкет:")
    await callback.message.edit_text(text, reply_markup=await FilterButton.filter_industy(
                                                                    callback.from_user.id, selected))


@router.callback_query(F.data.startswith("set_filter_"))
async def set_filter_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")

    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext
    industry = callback.data.split("_")[2]
    await state.update_data(industry_filter=industry)
    text = _("Фильтр установлен: {industry}.\nНажмите /show для поиска анкет.").format(industry=industry)
    await callback.message.edit_text(text)
    await callback.answer()


@router.callback_query(F.data == "reset_filter")
async def reset_filter_callback(callback: CallbackQuery, state: FSMContext):
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    await callback.answer("")

    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext
    await state.update_data(industry_filter=None)
    text = _("Фильтр сброшен. Теперь ищем все анкеты  \n/show")
    await callback.message.answer(text)
    await callback.answer()


@router.callback_query(F.data == "deactivate_anketa")
async def deactivate_callback(callback:CallbackQuery):
    await callback.answer("")

    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    user_id = callback.from_user.id

    try:
        await MetodSQL.set_profile_active(user_id, False)
        text = _("🚫 Анкета деактивирована.\n"
            "Желаем вам удачи в стартапе! 💡\n\n"
            "Чтобы снова включить анкету и искать партнёров — введите /activate")
        await callback.message.edit_text(
            text
        )
    except Exception:
        text = _("Произошла ошибка. Попробуйте позже.")
        await callback.message.answer(text)

    try:
        prof = profile(bot, user_id, callback.message.chat.id,
                       reply_mark=await ChangeRegister.changed_register(callback.from_user.id))
        if not prof:
            text = _("У вас покачто нету анкеты")
            await callback.message.answer(text)
        else:
            await prof
    except Exception:
        text = _("Произошла ошибка при загрузке профиля. Попробуйте снова позже.")
        await callback.message.answer(text)


@router.callback_query(F.data == "refcode")
async def refcode_handler(callback: CallbackQuery):
    await callback.answer("")

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
    ,reply_markup=await RefCode.refka_back(callback.from_user.id))


@router.callback_query(F.data == "language_lang")
async def language_hanlder(callback: CallbackQuery):
    await callback.answer("")

    await callback.message.delete()
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext
    lang_param = await MetodSQL.get_language(callback.from_user.id)

    translator = await get_translator(lang_param)
    _ = translator.gettext
    text = _("На каком языке вы хотели бы объединяться с другими ИТ-специалистами? 🌍")
    await callback.message.answer(
        text,
        reply_markup=await MetodKeyboardInline.lang_back(callback.from_user.id)
    )


@router.callback_query(lambda c: c.data in {
    "en", "es", "de",
    "uk", "ru",
    "kk", "ky", "it"
})
async def update_language(callback: CallbackQuery):
    await callback.answer("")

    lang_param = await MetodSQL.get_language(callback.from_user.id)

    translator = await get_translator(lang_param)
    _ = translator.gettext
    await MetodSQL.update_lang(callback.from_user.id, callback.data)
    text = _("Язык обновлен")
    await callback.message.answer(text)




