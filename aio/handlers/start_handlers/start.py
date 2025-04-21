from aio.keyboards.skip_param import SkipButton
from aio.validate.validate_register import ValidateParam
from aio.core.imports import *
import logging
from aio.services.match_service import send_profile_with_buttons
from aio.state.session_memory import likes_memory, liked_users, mutual_likes
from aio.services.match_service import proceed_to_next_profile
from aiogram.filters.command import Command, Message
from aiogram.fsm.context import FSMContext
from aio.keyboards.keyboard_for_start import MetodKeyboardInline
from database.metod_for_database import MetodSQL
from aio.context.context_fsm import RegisterState, CityRegister
from aio.handlers.routers.routers import dp
from aio.bot_token import bot
import asyncio
from aio.handlers.routers.router_for_start import router
from aiogram.types import ReplyKeyboardRemove, BufferedInputFile, CallbackQuery, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram import F
from aio.func.func_profile import profile
from aio.keyboards.keyboard_for_restart_register import ChangeRegister
from database.models import RegisterUser
from pydantic_schemas.unique_param import Param, ParamCity, ParamLarge
from aiogram.types import FSInputFile
import io
import logging
from cachetools import TTLCache
from aiogram.fsm.state import StatesGroup, State
import random
from aiogram import types
from aiogram.exceptions import TelegramAPIError, TelegramBadRequest
from cachetools import TTLCache
from aio.core.imports import *
import logging
from aio.handlers.filters import filter_handlers
from aio.handlers.filters import filter_handlers
import aio.handlers.show_handlers
from aio.services.match_service import send_profile_with_buttons
from aio.utils.cache import user_view_count, image_cache
from aio.state.session_memory import likes_memory, liked_users, mutual_likes, disliked_users
from aio.services.match_service import proceed_to_next_profile
import aio.handlers.filters.filter_handlers
import aio.handlers.show_handlers
import aio.handlers.profile_handlers
import aio.handlers.search_handlers
import aio.handlers.like_handlers
import aio.handlers.dislike_handlers
import aio.handlers.view_handlers
from database.models import Lang
from pydantic_schemas.unique_param import ParamLang
from text_translete.translate import get_translator
import gettext

logger = logging.getLogger(__name__)



@router.message(Command("deactivate"))
async def deactivate_profile(message: Message):
    lang_param = await MetodSQL.get_language(message.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    user_id = message.from_user.id

    try:
        await MetodSQL.set_profile_active(user_id, False)
        text = _("🚫 Анкета деактивирована.\n"
            "Желаем вам удачи в стартапе! 💡\n\n"
            "Чтобы снова включить анкету и искать партнёров — введите /activate")
        await message.answer(
            text
        )

    except Exception as e:
        logger.error(f"Ошибка при деактивации профиля: {e}")
        text = _("Произошла ошибка. Попробуйте позже.")
        await message.answer(text)


@router.message(Command("activate"))
async def activate_profile(message: Message):
    lang_param = await MetodSQL.get_language(message.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    user_id = message.from_user.id

    try:
        text = _("✅ Ваша анкета снова активна!\n"
            "Теперь другие пользователи смогут увидеть её и связаться с вами 🔍")
        await MetodSQL.set_profile_active(user_id, True)
        await message.answer(
          text
        )
    except Exception as e:
        logger.error(f"Ошибка при активации профиля: {e}")
        text = _("Произошла ошибка. Попробуйте позже.")
        await message.answer(text)



@router.callback_query(F.data == "skips")
async def skip_callback(callback: CallbackQuery, state: FSMContext):
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    data = await state.get_data()
    liked_users_in_session = data.get("liked_users",
                                      set())

    liked_users_in_session.add(callback.from_user.id)
    await state.update_data(liked_users=liked_users_in_session)
    await callback.message.delete()
    text = _("Анкета пропущена.")
    await callback.answer(text)
    await proceed_to_next_profile(state, callback)


async def check_likes_for_user(user_id: int):
    if user_id in liked_users and len(liked_users[user_id]) > 0:
        return True
    return False


@router.callback_query(F.data.startswith("next_profile_"))
async def next_profile_callback(callback: CallbackQuery, state: FSMContext):
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext


    data = await state.get_data()
    profiles = data.get("profiles", [])
    index = data.get("index", 0) + 1
    await callback.message.answer("👎")

    if index >= len(profiles):
        text = _("Анкеты закончились, подождите пока появятся новые и нажмите /show")
        await callback.message.answer(text)
        return

    user_id = callback.from_user.id
    if await check_likes_for_user(user_id):
        text = _("Ответьте на анкету, вас лайкнули!")
        await callback.message.answer(text)
        return
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception as e:
        logger.error(f"Ошибка при удалении кнопок: {e}")
    await state.update_data(index=index)
    await send_profile_with_buttons(callback.message.chat.id, profiles[index],index)
    await callback.answer()


@router.message(Command("start"))
async def language_start(message: Message):
    lang_param = await MetodSQL.get_language(message.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext
    res = await MetodSQL.see_true(message.from_user.id)
    print(res)
    if res:
        text = _("Ты уже зарегестрировался, чтобы увидеть анкету свою анкету нажмите /show")
        await message.answer(text)
        return
    await message.answer(
        "На каком языке вы хотели бы объединяться с другими ИТ-специалистами? 🌍",
        reply_markup=await MetodKeyboardInline.language_commnad()
    )

@router.callback_query(lambda c: c.data in {
    "en", "es", "de",
    "uk", "ru",
    "kk"
})
async def start_command(callback: CallbackQuery):
    lang = callback.data
    await MetodSQL.unieuq_add(ParamLang(user_name=callback.from_user.id, lang=lang), object_class=Lang)
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    user_id = callback.from_user.id
    user = int(user_id)
    prof = await MetodSQL.see_profile(user)

    if prof:
        await profile(bot, user, callback.message.chat.id, reply_mark=await ChangeRegister.changed_register(callback.from_user.id))
    else:
        text = _("🔥 <b>Приветствуем тебя в PairCode!</b> 🔥\n\n"
                 "🚀 Здесь ты сможешь найти напарника, помощника или единомышленника для совместной работы над проектами!\n"
                 "🤝 Объединяйся с профессионалами, делись идеями и создавай крутые вещи вместе!\n\n"
                 "💡 <b>PairCode</b> — это место, где начинаются великие проекты!\n\n"
                 "🎁 После регистрации ты сможешь <b>ввести реферальный код друга</b> или <b>поделиться своим</b>, используя команду <code>/ref</code>.\n\n"
                 "🛠 <b>Готов начать?</b> Тогда проходи регистрацию и начинай! 👇")

        await callback.message.edit_text(
            text,
            reply_markup=await MetodKeyboardInline.start_command(callback.from_user.id),
            parse_mode="HTML"
        )


@router.callback_query(F.data == "city")
async def location_city(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)

    print("Callback_Id",callback.from_user.id)
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)
    message = callback.message

    translator = await get_translator(lang_param)
    _ = translator.gettext

    text = _("Напишите из какого вы города ?🌆")

    await callback.message.answer(text)

    await state.set_state(CityRegister.city)

@router.message(CityRegister.city)
async def cite_detect(message: Message, state: FSMContext):
    print("User_id_message",message.from_user.id)
    lang_param = await MetodSQL.get_language(message.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    if not await ValidateParam.validate_city(message):
        return

    await state.update_data(city=message.text)

    await state.set_state(RegisterState.name)

    text = _("Как вас зовут?")
    await message.answer(text, reply_markup=ReplyKeyboardRemove())


@router.message(RegisterState.name)
async def register_name(message: Message, state:FSMContext):
    if not await ValidateParam.validate_name(message):
        return

    lang_param = await MetodSQL.get_language(message.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    await state.update_data(name=message.text)
    await state.set_state(RegisterState.age)
    text = _("Сколько вам лет ?🧓👵")
    await message.answer(text)


@router.message(RegisterState.age)
async def register_age(message: Message, state:FSMContext):

    if not await ValidateParam.validate_age(message):
        return

    lang_param = await MetodSQL.get_language(message.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    await state.update_data(age=message.text)
    await state.set_state(RegisterState.text_disc)
    text = _("Напишите описание для профиля🖊")
    await message.answer(text, reply_markup=await SkipButton.skip(message.from_user.id))



@router.message(RegisterState.text_disc)
async def register_discription(message: Message, state: FSMContext):

    if not await ValidateParam.validate_disc(message):
        return

    lang_param = await MetodSQL.get_language(message.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    await state.update_data(text_disc=message.text)
    await state.set_state(RegisterState.language)
    text = _("Какой у вас язык программирования?👨‍💻")
    await message.answer(text, reply_markup= await MetodKeyboardInline.language_button(message.from_user.id))


@router.message(RegisterState.language)
async def register_language(message:Message, state: FSMContext):
    await state.update_data(language=message.text)
    lang_param = await MetodSQL.get_language(message.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    if not await ValidateParam.validate_language(message):
        return

    safe_text = message.text.replace(')', '\\)').replace('(', '\\(')

    text = _("Вы выбрали {safe_text}, это точный ответ?").format(safe_text=safe_text)

    await message.answer(text, parse_mode="MarkdownV2", reply_markup=await MetodKeyboardInline.another_button(message.from_user.id))

@router.message(RegisterState.img)
async def register_img(message:Message, state: FSMContext):
    lang_param = await MetodSQL.get_language(message.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext

    if not await ValidateParam.validate_photo(message):
        return

    img = message.photo[-1].file_id

    file = await bot.download(img)
    img_bytes = file.read()

    await state.update_data(img=img_bytes)

    data = await state.get_data()
    user_name = message.from_user.id

    await asyncio.create_task(MetodSQL.unieuq_add(
        data=Param(
            user_name=user_name,
            city=data.get("city"),
            name=data.get("name"),
            age=data.get("age"),
            text_disc=data.get("text_disc"),
            language=data.get("language"),
            industry=data.get("industry"),
            img=data.get("img")
        ),
        object_class=RegisterUser
    ))
    await state.clear()
    text = _("""
    Ты зарегестрировался !
От как выглядит твоя анкета!""")
    await message.answer(text)

    user_id = message.from_user.id
    user = int(user_id)

    await state.clear()
    await profile(bot,user, message.chat.id, reply_mark=await ChangeRegister.changed_register(message.from_user.id))



async def main_context():
    await dp.start_polling(bot, debug=True)

