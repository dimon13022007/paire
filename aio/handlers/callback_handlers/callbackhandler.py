from aiogram import F, Router
from aiogram.types import CallbackQuery
from aio.context.context_fsm import RegisterState
from aiogram.fsm.context import FSMContext
from aio.keyboards.keyboard_for_start import MetodKeyboardInline
from aio.context.context_new_value import NewValue
import logging
from database.metod_for_database import MetodSQL
from aiogram.types import Message
from text_translete.translate import get_translator
import gettext

router = Router(name=__name__)

logging.basicConfig(level=logging.INFO)


@router.callback_query(lambda c: c.data in {
    "Python", "Java", "JavaScript", "PHP", "Go",
    "C,C++", "C#", "Swift", "Kotlin", "R"
})
async def language_callback(callback_query: CallbackQuery, state: FSMContext):

    lang_param = await MetodSQL.get_language(callback_query.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    data = await state.get_data()
    selected = data.get("language", [])
    if not isinstance(selected, list):
        selected = []
        print("Ti dayn?")

    language = callback_query.data

    if language in selected:
        selected.remove(language)
    elif len(selected) < 2:
        selected.append(language)
    else:
        text = _("Максимум 2")
        await callback_query.answer(text)
        return


    await state.update_data(language=selected)
    await callback_query.message.edit_text("Какой у вас язык программирования ?",
                                        reply_markup=await MetodKeyboardInline.language_button(
                                            callback_query.from_user.id,selected
                                        ))

@router.callback_query(F.data == "success")
async def nice_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    translator = await get_translator(lang_param)
    _ = translator.gettext
    data = await state.get_data()

    selected_lang = data.get("language", [])

    if not selected_lang:
        await callback.answer(_("Выберите хотя бы один язык"))
        return
    try:
        logging.info("Остался в том же состоянии")
        # не перезаписуємо language!
        # await state.update_data(language=callback.data) <-- Удалить или закомментировать

        text = _(f"Твой язык {', '.join(selected_lang)}")
        await callback.answer(text)
        await state.set_state(RegisterState.industry)

        text2 = _("Выберите индустрии, повторное нажатие снимает выбор:")
        selected = data.get("industries", [])
        await callback.message.edit_text(
            text2,
            reply_markup=await MetodKeyboardInline.industry_button(callback.from_user.id,selected)
        )

    except Exception as err:
        logging.error(f"Ошибка в обработке выбора языка: {err}", exc_info=True)
        text = _("❌ Произошла ошибка. Попробуйте еще раз.")
        await callback.answer(text)


# @router.callback_query(F.data == "Другое")
# async def anothe_callback(callback_query: CallbackQuery, state: FSMContext):
#     await callback_query.answer("")
#
#     lang_param = await MetodSQL.get_language(callback_query.from_user.id)
#     print(lang_param)
#
#     translator = await get_translator(lang_param)
#     _ = translator.gettext
#
#     text = _("Напишите на каком языке вы пишете")
#     await callback_query.message.edit_text(text)
#     await callback_query.answer("")
#     await state.set_state(RegisterState.language)


# @router.callback_query(F.data == "Yes")
# async def anothe_callback_yes(callback_query: CallbackQuery, state: FSMContext):
#     await callback_query.answer("")
#
#     lang_param = await MetodSQL.get_language(callback_query.from_user.id)
#     print(lang_param)
#
#     translator = await get_translator(lang_param)
#     _ = translator.gettext
#
#     data = await state.get_data()
#     user_lang = data.get("language")
#     await callback_query.answer("")
#     await state.set_state(RegisterState.industry)
#     text = _("Чем вы занимаетесь?")
#     await callback_query.message.edit_text(text, reply_markup=await MetodKeyboardInline.industry_button())
#
#
# @router.callback_query(F.data == "change")
# async def another_callback_no(callback_query: CallbackQuery, state: FSMContext):
#     await callback_query.answer("")
#
#     lang_param = await MetodSQL.get_language(callback_query.from_user.id)
#     print(lang_param)
#
#     translator = await get_translator(lang_param)
#     _ = translator.gettext
#
#     text = _("Напишите на каком языке вы пишете")
#     await callback_query.message.edit_text(text)
#     await callback_query.answer("")
#     await state.set_state(RegisterState.language)
