from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from database.metod_for_database import MetodSQL
from aio.keyboards.keyboard_change import ChangeAnketa
from aio.context.context_new_value import NewValue
import logging
from aio.func.func_profile import profile
from aio.keyboards.keyboard_for_restart_register import ChangeRegister
from aio.bot_token import bot
from aio.validate.validate_register import ValidateParam
from text_translete.translate import get_translator
import gettext

router = Router()

logging.basicConfig(level=logging.INFO)

@router.callback_query(F.data == "change_param")
async def change_param(callback: CallbackQuery):
    await callback.answer("")

    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext
    text = _("Выбирете какой именно параметр хотите изменить")
    await callback.message.answer(text, reply_markup= await ChangeAnketa.changed_register(callback.from_user.id))


@router.callback_query(lambda c: c.data in {"change_city","change_name", "change_age", "change_text_disc",
                                            "change_lang", "change_industry", "change_img"})
async def change_param(callback: CallbackQuery, state: FSMContext):
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    await callback.answer("")


    callback_abbr = {
        "change_city": "city",
        "change_name": "name",
        "change_age": "age",
        "change_text_disc": "text_disc",
        "change_lang": "language",
        "change_industry": "industry",
        "change_img": "img",
    }
    field_name = callback_abbr.get(callback.data)

    if not field_name:
        text = _("❌ Такого параметра для изменения не существует 😉")
        await callback.message.answer(text)
        await callback.answer()
        return

    result = await MetodSQL.update(user_id=callback.from_user.id, field_name=field_name)

    await state.update_data(field_name=field_name)

    if field_name in "city":
        text = _("Введите новое значение для {field}\nТекущее: {current}").format(field=field_name, current=result)
        await callback.message.answer(text)
        await state.set_state(NewValue.new_value)

    if field_name in "name":
        text = _("Введите новое значение для {field}\nТекущее: {current}").format(field=field_name, current=result)
        await callback.message.answer(text)
        await state.set_state(NewValue.new_value)

    if field_name in "age":
        await state.set_state(NewValue.new_value)

    if field_name in "text_disc":
        text = _("Введите новое значение для {field}\nТекущее: {current}").format(field=field_name, current=result)
        await callback.message.answer(text)
        await state.set_state(NewValue.new_value)

    if field_name in "language":
        text = _("Введите новое значение для {field}\nТекущее: {current}").format(field=field_name, current=result)
        await callback.message.answer(text)
        await state.set_state(NewValue.new_value)

    elif field_name == "industry":
        text = _(
            "Какое новое значение вы хотите определить?\nТекущее {current}\n"
            "1) Backend\n2) Front-end\n3) FullStack\n4) GameDev\n5) MobileDev"
        ).format(current=result)
        await callback.message.answer(text)
        await state.set_state(NewValue.new_value)

    elif field_name == "img":
        text = _("Загрузите новое изображение📸")
        await callback.message.answer(text)
        await state.set_state(NewValue.new_value)


@router.message(NewValue.new_value)
async def new_value(message: Message, state: FSMContext):
    lang_param = await MetodSQL.get_language(message.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    user_data = await state.get_data()
    field_name = user_data.get("field_name")

    try:
        if field_name in "name":
            if not await ValidateParam.validate_name(message):
                return

        if field_name in "city":
            if not await ValidateParam.validate_city(message):
                return

        if field_name in "age":
            try:
                age = int(message.text)

                if not await ValidateParam.validate_age(message):
                    return

                result = await MetodSQL.update(user_id=message.from_user.id, field_name=field_name, new_value=str(age))

                if result:
                    text = _("Ваш возраст обновлен: {age} ✅").format(age=age)
                    await message.answer(text)
                    user = int(message.from_user.id)
                    await profile(bot, user, message.chat.id, reply_mark=await ChangeRegister.changed_register(user))
                    return
                else:
                    text = _("❌ Не удалось обновить возраст. Пожалуйста, попробуйте снова.")
                    await message.answer(text)
                    return

            except ValueError:
                text = _("❌ Пожалуйста, введите корректный возраст (целое число).")
                await message.answer(text)
                return

        if field_name in "text_disc":
            if not await ValidateParam.validate_disc(message):
                return

        if field_name == "language":
            if not await ValidateParam.validate_language(message):
                return

            new_language = message.text

            result = await MetodSQL.update(user_id=message.from_user.id, field_name=field_name, new_value=new_language)

            if result:
                text = _("Ваш язык успешно обновлен: {language} ✅").format(language=new_language)
                await message.answer(text)
                user_id = message.from_user.id
                user = int(user_id)
                await profile(bot, user, message.chat.id,
                              reply_mark=await ChangeRegister.changed_register(message.from_user.id))
            else:
                text = _("❌ Не удалось обновить язык. Пожалуйста, попробуйте снова.")
                await message.answer(text)



        elif field_name == "img":
            if not message.photo:
                text = _("❌ Вы не отправили фото. Пожалуйста, отправьте фото.")
                await message.answer(text)
                return

            photo = message.photo[-1]

            if not photo or not isinstance(photo.file_id, str):
                text = _("❌ Произошла ошибка при обработке фото, попробуйте снова.")
                await message.answer(text)
                return

            try:
                file_info = await message.bot.get_file(photo.file_id)
                file = await message.bot.download_file(file_info.file_path)
                img_bytes = file.read()

                await state.update_data(img=img_bytes)

                result = await MetodSQL.update(user_id=message.from_user.id, field_name=field_name, new_value=img_bytes)

                if result:
                    text = _("✅ Изображение успешно обновлено!")
                    await message.answer(text)
                    user_id = message.from_user.id
                    user = int(user_id)
                    await profile(bot, user, message.chat.id, reply_mark=await ChangeRegister.changed_register(message.from_user.id))
                else:
                    logging.error(
                        f"Ошибка при обновлении {field_name} для пользователя {message.from_user.id}. Новый параметр: {img_bytes}. Результат: {result}")
                    await message.answer("❌ Не удалось обновить изображение. Попробуйте снова.")
            except Exception as e:
                logging.error(f"Ошибка при обработке изображения: {e}")
                text = _("❌ Произошла ошибка при обработке изображения, попробуйте снова.")
                await message.answer(text)


        elif field_name == "industry":
            ind = {
                1: "Backend",
                2: "Front-end",
                3: "FullStack",
                4: "GameDev",
                5: "MobileDev"
            }
            try:

                industry_choice = int(message.text)

                if industry_choice in ind:
                    industry_value = ind[industry_choice]

                    result = await MetodSQL.update(user_id=message.from_user.id, field_name=field_name,
                                                   new_value=industry_value)
                    if result:
                        text = _("Вы выбрали индустрию: {industry_value} ✅").format(industry_value=industry_value)
                        await message.answer(text)
                        user_id = message.from_user.id
                        user = int(user_id)
                        await profile(bot, user, message.chat.id, reply_mark=await ChangeRegister.changed_register(message.from_user.id))
                    else:
                        text = _("❌ Не удалось обновить индустрию. Пожалуйста, попробуйте снова.")
                        await message.answer(text)
                        return
                else:
                    text = _("❌ Неверный выбор! Пожалуйста, выберите число от 1 до 5.")
                    await message.answer(text)
                    return

            except ValueError:
                text = _("❌ Пожалуйста, введите число от 1 до 5.")
                await message.answer(text)

        else:
            new_value = message.text

            result = await MetodSQL.update(user_id=message.from_user.id, field_name=field_name, new_value=new_value)

            if result:
                text = _("Обновление прошло успешно ✅")
                await message.answer(text)
                user_id = message.from_user.id
                user = int(user_id)
                await profile(bot, user, message.chat.id, reply_mark=await ChangeRegister.changed_register(message.from_user.id))
            else:
                logging.error(f"Ошибка при обновлении {field_name} для пользователя {message.from_user.id}. Новый параметр: {new_value}. Результат: {result}")
                text = _("С обновлением возникли трудности 😢")
                await message.answer(text)


    except Exception as err:
        logging.error(f"Не удалось обновить {field_name} для пользователя {message.from_user.id}. Ошибка: {str(err)}")
        text = _(f"❌ Произошла ошибка. Пожалуйста, попробуйте снова.1")
        await message.answer(text)

    await state.clear()


