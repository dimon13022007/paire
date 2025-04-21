from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aio.utils.cache import user_view_count
from aio.utils.media import get_image, send_advertisement
from aio.bot_token import bot
from aiogram.exceptions import TelegramAPIError
import logging
from text_translete.translate import get_translator
import gettext
from database.metod_for_database import MetodSQL
import time
import asyncio

logger = logging.getLogger(__name__)


async def send_profile_with_buttons(chat_id: int, profile, index: int):
    start = time.time()
    user_id = chat_id
    view_count = user_view_count.get(user_id, 0)

    logger.info(f"[{user_id}] ▶ Отправляем анкету #{index}")
    logger.debug(f"[{user_id}] 📊 view_count = {view_count}")
    logger.debug(f"[{user_id}] 👤 Текст анкеты: {profile.city}\n{profile.name} ({profile.age})\n{profile.industry} | {profile.language}, {profile.text_disc or ''}")

    profile_text = f"{profile.city}\n{profile.name} ({profile.age})\n{profile.industry} | {profile.language}"
    if profile.text_disc:
        profile_text += f", {profile.text_disc}"

    like_button = InlineKeyboardButton(text="👍", callback_data=f"like_{profile.user_name}")
    dislike_button = InlineKeyboardButton(text="👎", callback_data=f"next_profile_{index}")
    sleep_button = InlineKeyboardButton(text="💤", callback_data="show_profile")
    report_button = InlineKeyboardButton(text="🚫", callback_data=f"report_{profile.user_name}")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[like_button, dislike_button, sleep_button, report_button]],)

    if profile.img:
        logger.debug(f"[{user_id}] 🖼️ Изображение найдено, получаем...")
        img_start = time.time()
        img_file = await get_image(profile.img)
        logger.debug(f"[{user_id}] ⏱ get_image: {round((time.time() - img_start) * 1000)} ms")

        if img_file:
            try:
                send_start = time.time()
                await asyncio.sleep(0.05)  # 🧘 Анти-флуд
                await bot.send_photo(chat_id, photo=img_file, caption=profile_text, reply_markup=keyboard, parse_mode="HTML")
                logger.debug(f"[{user_id}] 📤 Фото отправлено за {round((time.time() - send_start) * 1000)} ms")
            except TelegramAPIError as e:
                logger.warning(f"[{user_id}] ⚠️ Ошибка Telegram API: {e}")
                await bot.send_message(chat_id, f"Ошибка при загрузке фото {profile.name}.", reply_markup=keyboard)
        else:
            logger.warning(f"[{user_id}] ❌ Не удалось загрузить изображение")
            await bot.send_message(chat_id, "Ошибка при загрузке фото.", reply_markup=keyboard)
    else:
        logger.debug(f"[{user_id}] 📄 Отправляем анкету без фото")
        text_send_start = time.time()
        try:
            await asyncio.sleep(0.05)
            await bot.send_message(chat_id, profile_text, reply_markup=keyboard, parse_mode="HTML")
        except TelegramAPIError as e:
            logger.warning(f"[{user_id}] ❌ Ошибка при отправке анкеты: {e}")
            await bot.send_message(chat_id, "🚨 Ошибка при показе анкеты. Попробуйте позже.")
        logger.debug(f"[{user_id}] 💬 Сообщение отправлено за {round((time.time() - text_send_start) * 1000)} ms")

    logger.info(f"[{user_id}] ✅ Анкета отправлена за {round((time.time() - start) * 1000)} ms")
    user_view_count[user_id] = view_count + 1




async def proceed_to_next_profile(state: FSMContext, callback: CallbackQuery):
    start_time = time.time()
    user_id = callback.from_user.id

    logger.debug(f"[{user_id}] 🔁 Запуск proceed_to_next_profile")

    lang_param = await MetodSQL.get_language(user_id)
    translator = await get_translator(lang_param)
    _ = translator.gettext

    data = await state.get_data()
    profiles = data.get("profiles", [])
    index = data.get("index", 0) + 1

    logger.debug(f"[{user_id}] 📄 Текущий индекс: {index}/{len(profiles)}")

    if index >= len(profiles):
        logger.debug(f"[{user_id}] 🧭 Переход к новым анкетам (старые закончились)")

        t_search = time.time()
        industry_filter = data.get("industry_filter")
        new_profiles = await MetodSQL.search_profiles(
            exclude_user_id=user_id,
            industry=industry_filter
        )
        logger.debug(f"[{user_id}] 🔎 Поиск новых анкет занял {round((time.time() - t_search) * 1000)} ms")

        if not new_profiles:
            await callback.message.answer(_("Анкеты закончились, подождите пока появятся новые и нажмите /show"))
            return

        profiles = new_profiles
        index = 0
        await state.update_data(profiles=profiles, index=index)
    else:
        await state.update_data(index=index)

    logger.debug(f"[{user_id}] ⬇ Переход к анкете #{index}")
    await asyncio.sleep(0.01)
    await send_profile_with_buttons(callback.message.chat.id, profiles[index], index)

    duration = round((time.time() - start_time) * 1000)
    logger.info(f"[{user_id}] ⏱ Переход завершён за {duration} ms")


