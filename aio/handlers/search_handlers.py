from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram import F
from aio.services.match_service import send_profile_with_buttons
from database.metod_for_database import MetodSQL
from aio.state.session_memory import liked_users
import logging
import random
from aiogram import Router
from text_translete.translate import get_translator
import gettext
from database.session import async_session

router = Router()

logger = logging.getLogger(__name__)

@router.callback_query(F.data == "search")
async def search_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    user_id = callback.from_user.id

    async with async_session() as session:
        if await MetodSQL.is_blocked(session, user_id):
            await callback.message.answer("🚫 Вы были заблокированы и не можете продолжать пользоваться ботом.")
            return

    lang_param = await MetodSQL.get_language(user_id)
    translator = await get_translator(lang_param)
    _ = translator.gettext

    await callback.message.answer("🔍✨")

    try:
        data = await state.get_data()
        liked_users_in_session = data.get("liked_users", set())

        if user_id in liked_users and liked_users[user_id] and user_id not in liked_users_in_session:
            liker_id = next(iter(liked_users[user_id]))
            await callback.message.answer(
                _("Ответьте на анкету, вас лайкнули!"),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text=_("Посмотреть анкету"), callback_data=f"view_{liker_id}")]
                ])
            )
            return

        try:
            if callback.message.reply_markup:
                new_keyboard = [
                    [btn for btn in row if btn.text != _("Продолжить просмотр анкет")]
                    for row in callback.message.reply_markup.inline_keyboard
                ]
                if new_keyboard != callback.message.reply_markup.inline_keyboard:
                    await callback.message.edit_reply_markup(
                        reply_markup=InlineKeyboardMarkup(inline_keyboard=new_keyboard))
            await callback.answer(_("Продолжаем просмотр анкет..."))
        except Exception as e:
            logger.warning(f"Не удалось обновить клавиатуру: {e}")

        liked_users.pop(user_id, None)

        # industry_filter = data.get("industry_filter")
        industry_filter = await MetodSQL.see_filter(callback.from_user.id)

        if industry_filter:
            profiles = await MetodSQL.search_profiles(exclude_user_id=user_id, industry=industry_filter)
        else:
            profiles = await MetodSQL.search_profiles(exclude_user_id=user_id)

        if not profiles:
            await callback.message.answer(
                _(f"Нет анкет в категории {industry_filter} 😔" if industry_filter else "Нет найденных анкет")
            )
            return

        await state.update_data(profiles=profiles, index=0, page=0)

        logger.info(f"Найдено анкет: {len(profiles)} для пользователя {user_id}")
        await send_profile_with_buttons(callback.message.chat.id, profiles[0], 0)

    except Exception as e:
        logger.error(f"Ошибка при поиске анкет для {user_id}: {e}")
        await callback.message.answer(_("Произошла ошибка при поиске анкет."))
