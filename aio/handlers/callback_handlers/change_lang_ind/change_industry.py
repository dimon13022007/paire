from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from database.metod_for_database import MetodSQL
from aio.func.func_profile import profile
from aio.keyboards.keyboard_for_restart_register import ChangeRegister
from aio.bot_token import bot
from text_translete.translate import get_translator
from aio.context.context_for_ind import IndustryState, LangState
from aio.validate.validate_register import ValidateParam

router = Router()

@router.callback_query(F.data.in_({"ind2", "ind3"}))
async def change_industry(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        field_map = {
            "ind2": "industry_1",
            "ind3": "industry_2"
        }

        field_name = field_map.get(callback.data)
        if not field_name:
            await callback.message.answer("❌ Невідомий параметр.")
            return

        lang_param = await MetodSQL.get_language(callback.from_user.id)
        translator = await get_translator(lang_param)
        _ = translator.gettext

        await state.update_data(field_name=field_name)
        await state.set_state(IndustryState.waiting_for_industry_choice)

        if field_name == "industry":
            await callback.message.answer(_("❌ Нельзя очистить поле индустрии. Пожалуйста, выберите новое значение."))
            return

        current = await MetodSQL.update(user_id=callback.from_user.id, field_name=field_name, new_value=None)

        text = _(
            "Какое новое значение вы хотите определить?\nТекущее: {current}\n"
            "1) Backend\n"
            "2) Front-end\n"
            "3) FullStack\n"
            "4) GameDev\n"
            "5) MobileDev\n"
            "6) AIDev\n"
            "7) Telegram Bots\n"
            "8) AppDev\n"
            "9) OSDev\n"
            "10) Cybersecurity\n"
            "11) Frameworks\n"
            "12) BlockchainDev\n"
            "13) Удалить индустрию"
            "✍️ Напиши номер индустрии сообщением."
        ).format(current=current)

        await callback.message.answer(text)
        await state.update_data(field_name=field_name)

    except Exception as e:
        await callback.message.answer(f"❌ Ошибка при обработке callback: {str(e)}")


@router.message(IndustryState.waiting_for_industry_choice)
async def save_industry_choice(message: Message, state: FSMContext):
    try:
        user_data = await state.get_data()
        field_name = user_data.get("field_name")

        if not field_name:
            await message.answer("⚠️ Нет выбранного поля. Пожалуйста, начните сначала.")
            return

        lang_param = await MetodSQL.get_language(message.from_user.id)
        translator = await get_translator(lang_param)
        _ = translator.gettext

        ind = {
            1: "Backend",
            2: "Front-end",
            3: "FullStack",
            4: "GameDev",
            5: "MobileDev",
            6: "AIDev",
            7: "Telegram Bots",
            8: "AppDev",
            9: "OSDev",
            10: "Cybersecurity",
            11: "Frameworks",
            12: "BlockchainDev",
            13: None
        }

        try:
            industry_choice = int(message.text)

            if industry_choice in ind:
                industry_value = ind[industry_choice]
            else:
                await message.answer(_("❌ Неверный выбор! Пожалуйста, выберите число от 1 до 12."))
                return

            result = await MetodSQL.update_none(
                user_id=message.from_user.id,
                field_name=field_name,
                new_value=industry_value
            )

            if result:
                text = (
                    _("Вы убрали выбор индустрии ✅") if industry_value is None
                    else _("Вы выбрали индустрию: {industry_value} ✅").format(industry_value=industry_value)
                )
                await message.answer(text)

                await profile(
                    bot,
                    message.from_user.id,
                    message.chat.id,
                    reply_mark=await ChangeRegister.changed_register(message.from_user.id)
                )
            else:
                await message.answer(_("❌ Не удалось обновить индустрию. Попробуйте снова."))

            await state.clear()

        except ValueError as e:
            await message.answer(f"❌ Ошибка в выборе индустрии: {str(e)}")

    except Exception as e:
        await message.answer(f"❌ Ошибка при обработке сообщения: {str(e)}")


@router.callback_query(F.data.in_({"ind1"}))
async def change_industry(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    field_map = {
        "ind1": "industry",
    }

    field_name = field_map.get(callback.data)
    if not field_name:
        await callback.message.answer("❌ Невідомий параметр.")
        return

    lang_param = await MetodSQL.get_language(callback.from_user.id)
    translator = await get_translator(lang_param)
    _ = translator.gettext

    await state.update_data(field_name=field_name)
    await state.set_state(IndustryState.waiting_for_industry_choice)

    current = await MetodSQL.update(user_id=callback.from_user.id, field_name=field_name, new_value=None)

    text = _(
        "Какое новое значение вы хотите определить?\nТекущее: {current}\n"
        "1) Backend\n"
        "2) Front-end\n"
        "3) FullStack\n"
        "4) GameDev\n"
        "5) MobileDev\n"
        "6) AIDev\n"
        "7) Telegram Bots\n"
        "8) AppDev\n"
        "9) OSDev\n"
        "10) Cybersecurity\n"
        "11) Frameworks\n"
        "12) BlockchainDev\n"
        "✍️ Напиши номер индустрии сообщением."
    ).format(current=current)

    await callback.message.answer(text)
    await state.update_data(field_name=field_name)


@router.message(IndustryState.waiting_for_industry_choice)
async def save_industry_choice(message: Message, state: FSMContext):
    user_data = await state.get_data()
    field_name = user_data.get("field_name")

    if not field_name:
        await message.answer("⚠️ Нет выбранного поля. Пожалуйста, начните сначала.")
        return

    lang_param = await MetodSQL.get_language(message.from_user.id)
    translator = await get_translator(lang_param)
    _ = translator.gettext

    ind = {
        1: "Backend",
        2: "Front-end",
        3: "FullStack",
        4: "GameDev",
        5: "MobileDev",
        6: "AIDev",
        7: "Telegram Bots",
        8: "AppDev",
        9: "OSDev",
        10: "Cybersecurity",
        11: "Frameworks",
        12: "BlockchainDev",
    }

    try:
        industry_choice = int(message.text)


        if industry_choice in ind:
            industry_value = ind[industry_choice]
        else:
            await message.answer(_("❌ Неверный выбор! Пожалуйста, выберите число от 1 до 12."))
            return

        result = await MetodSQL.update(
            user_id=message.from_user.id,
            field_name=field_name,
            new_value=industry_value
        )

        if result:
            await message.answer(_("Вы выбрали индустрию: {industry_value} ✅").format(industry_value=industry_value))
            await profile(
                bot,
                message.from_user.id,
                message.chat.id,
                reply_mark=await ChangeRegister.changed_register(message.from_user.id)
            )
        else:
            await message.answer(_("❌ Не удалось обновить индустрию. Попробуйте снова."))

        await state.clear()

    except ValueError:
        await message.answer(_("❌ Пожалуйста, введите число от 1 до 13."))




@router.callback_query(F.data == "lang1")
async def lang_first_change(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    translator = await get_translator(lang_param)
    _ = translator.gettext

    user_data = await state.get_data()
    field_name = user_data.get("field_name")

    await callback.message.answer(f"Введите новое значение для {field_name}")
    await state.set_state(LangState.waiting_for_lang_choice)
    await state.update_data(field_name=field_name)



@router.message(LangState.waiting_for_lang_choice)
async def state_language(message: Message, state: FSMContext):
    lang_param = await MetodSQL.get_language(message.from_user.id)
    translator = await get_translator(lang_param)
    _ = translator.gettext

    user_data = await state.get_data()
    field_name = user_data.get("field_name")
    await state.update_data(field_name=field_name)

    new_language = message.text
    if not await ValidateParam.validate_language(message):
        return

    result = await MetodSQL.update(
        user_id=message.from_user.id,
        field_name=field_name,
        new_value=new_language
    )

    if result:
        await message.answer(_("Ваше значення мови оновлено: {new_language} ✅").format(new_language=new_language))
        await profile(
            bot,
            message.from_user.id,
            message.chat.id,
            reply_mark=await ChangeRegister.changed_register(message.from_user.id)
        )
    else:
        await message.answer(_("❌ Не вдалося оновити мову. Спробуйте ще раз."))

    await state.clear()




@router.callback_query(F.data == "lang2")
async def lang_second_change(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    translator = await get_translator(lang_param)
    _ = translator.gettext

    user_data = await state.get_data()
    field_name = user_data.get("field_name")

    await callback.message.answer(f"Введите новое значение для {field_name}")
    await state.set_state(LangState.waiting_for_lang_choice)
    await state.update_data(field_name="language_2")


@router.message(LangState.waiting_for_lang_choice)
async def state_language_second(message: Message, state: FSMContext):
    lang_param = await MetodSQL.get_language(message.from_user.id)
    translator = await get_translator(lang_param)
    _ = translator.gettext

    user_data = await state.get_data()
    field_name = user_data.get("field_name")

    new_language = message.text

    if not await ValidateParam.validate_language(message):
        return

    result = await MetodSQL.update(
        user_id=message.from_user.id,
        field_name=field_name,
        new_value=new_language
    )
    if result:
        await message.answer(_("Ваше значення мови оновлено: {new_language} ✅").format(new_language=new_language))
        await profile(
            bot,
            message.from_user.id,
            message.chat.id,
            reply_mark=await ChangeRegister.changed_register(message.from_user.id)
        )

    else:
        await message.answer(_("❌ Не вдалося оновити мову. Спробуйте ще раз."))

    await state.clear()

