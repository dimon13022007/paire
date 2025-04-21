from aiogram.types import CallbackQuery, Message
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aio.context.context_change import ChangeRegisterParam
from aio.keyboards.keyboard_for_start import MetodKeyboardInline
from aio.bot_token import bot
from database.metod_for_database import MetodSQL
from aio.func.func_profile import profile
from pydantic_schemas.unique_param import Param
from database.models import RegisterUser
from aio.keyboards.skip_param import SkipButton
from aio.validate.validate_register import ValidateParam
from text_translete.translate import get_translator
import gettext

router = Router()

@router.callback_query(F.data == "change_anketa")
async def change_anketa(callback: CallbackQuery, state: FSMContext):
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    await callback.answer("")

    text = _("Введите свой город еще раз🌆")
    await callback.message.answer(text)
    await state.set_state(ChangeRegisterParam.city)

@router.message(ChangeRegisterParam.city)
async def change_name(message: Message, state: FSMContext):
    lang_param = await MetodSQL.get_language(message.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    if not await ValidateParam.validate_city(message):
        return

    await state.update_data(city=message.text)
    await state.set_state(ChangeRegisterParam.name)
    text = _("Введите ваше имя еще раз")
    await message.answer(text)


@router.message(ChangeRegisterParam.name)
async def change_name(message: Message, state: FSMContext):
    lang_param = await MetodSQL.get_language(message.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    if not await ValidateParam.validate_name(message):
        return

    await state.update_data(name=message.text)
    await state.set_state(ChangeRegisterParam.age)
    text = _("Введите ваш возраст")
    await message.answer(text)

@router.message(ChangeRegisterParam.age)
async def change_age(message: Message, state: FSMContext):
    lang_param = await MetodSQL.get_language(message.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    if not await ValidateParam.validate_age(message):
        return

    age = str(message.text)
    await state.update_data(age=age)
    await state.set_state(ChangeRegisterParam.text_disc)
    text = _("Введите новое описание🖊")
    await message.answer(text, reply_markup=await SkipButton.skip(message.from_user.id))


@router.message(ChangeRegisterParam.text_disc)
async def change_text(message: Message, state: FSMContext):
    lang_param = await MetodSQL.get_language(message.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    if not await ValidateParam.validate_disc(message):
        return

    await state.update_data(text_disc=message.text)
    await state.set_state(ChangeRegisterParam.language)
    text = _("Какой у вас язык программирования?")
    await message.answer(text, reply_markup= await MetodKeyboardInline.language_button(message.from_user.id))

@router.message(ChangeRegisterParam.language)
async def change_lang(message: Message, state: FSMContext):
    lang_param = await MetodSQL.get_language(message.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    if not await ValidateParam.validate_language(message):
        return

    await state.update_data(language=message.text)
    await state.set_state(ChangeRegisterParam.industry)
    text = _("Какое у вас направление?")
    await message.answer(text, reply_markup=await MetodKeyboardInline.industry_button())

@router.message(ChangeRegisterParam.industry)
async def change_ind(message:Message, state: FSMContext):
    lang_param = await MetodSQL.get_language(message.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    await state.update_data(industry=message.text)
    await state.set_state(ChangeRegisterParam.industry)
    text = _("Добавьте фото профиля📸")
    await message.answer(text)

@router.message(ChangeRegisterParam.img)
async def register_img(message: Message, state: FSMContext):
    img = message.photo[-1].file_id

    file = await bot.download(img)
    img_bytes = file.read()

    await state.update_data(img=img_bytes)

    data = await state.get_data()
    user_name = message.from_user.id

    await MetodSQL.unieuq_add(
        data=Param(
            user_name=user_name,
            city=data.get("city"),
            name=data.get("name"),
            age= data.get("age"),
            text_disc=data.get("text_disc"),
            language=data.get("language"),
            industry=data.get("industry"),
            img=data.get("img"),
        ),
        object_class=RegisterUser
    )

    print("Success Update")

    await state.clear()
    lang_param = await MetodSQL.get_language(message.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    text = _("Ты перезарегистрировался! Вот как выглядит твоя анкета.")
    await message.answer(text)

    user_id = message.from_user.id
    await profile(bot, user_id, message.chat.id)







