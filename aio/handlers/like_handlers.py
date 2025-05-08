from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram import F
from aio.handlers.routers.router_for_start import router
from aio.handlers.start_handlers.start import proceed_to_next_profile
from database.metod_for_database import MetodSQL
from aio.state.session_memory import likes_memory, liked_users, mutual_likes, disliked_users
from aio.bot_token import bot
import logging
from database.metod_for_database import MetodSQL
from text_translete.translate import get_translator
import gettext

logger = logging.getLogger(__name__)


def build_profile_text(profile) -> str:
    if not profile.text_disc:
        return f"{profile.name} ({profile.age})\n{profile.industry} | {profile.language}, {profile.city}"
    return f"{profile.name} ({profile.age})\n{profile.industry} | {profile.language}, {profile.text_disc}, {profile.city}"


@router.callback_query(F.data.startswith("like_"))
async def like_callback(callback: CallbackQuery, state: FSMContext):
    liker_id = callback.from_user.id
    liked_id = int(callback.data.split("_")[1])

    should_continue = True

    try:
        await bot.send_message(liker_id, "👍")
    except Exception as e:
        logger.warning(f"Не удалось отправить эмодзи лайка: {e}")

    try:
        liker_lang_param = await MetodSQL.get_language(liker_id)
        liked_lang_param = await MetodSQL.get_language(liked_id)

        liker_translator = await get_translator(liker_lang_param)
        liked_translator = await get_translator(liked_lang_param)

        _ = liker_translator.gettext
        __ = liked_translator.gettext

        likes_memory.setdefault(liker_id, set()).add(liked_id)
        liked_users.setdefault(liked_id, set()).add(liker_id)

        mutual = liked_id in likes_memory and liker_id in likes_memory[liked_id]

        if mutual and liked_id not in disliked_users.get(liker_id, set()) and liker_id not in disliked_users.get(liked_id, set()):
            should_continue = False

            MetodSQL.mark_mutual(liker_id, liked_id)

            liker = await MetodSQL.get_user_by_id(liker_id)
            liked = await MetodSQL.get_user_by_id(liked_id)

            liker_profile_text = build_profile_text(liker)
            liked_profile_text = build_profile_text(liked)

            liker_img = BufferedInputFile(liker.img, filename="liker.jpg") if liker.img else None
            liked_img = BufferedInputFile(liked.img, filename="liked.jpg") if liked.img else None

            mutual_like_markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=_("🔁 Продолжить просмотр анкет"), callback_data="search")],
                [InlineKeyboardButton(text=_("👤 Перейти в профиль"), url=f"tg://user?id={liked_id}")]
            ])

            mutual_like_markup_for_liked = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=__("🔁 Продолжить просмотр анкет"), callback_data="search")],
                [InlineKeyboardButton(text=__("👤 Перейти в профиль"), url=f"tg://user?id={liker_id}")]
            ])

            await bot.send_message(liker_id, _("✨ У вас взаимный лайк с {name}!").format(name=liked.name))

            try:
                await bot.send_message(liked_id, __("✨ У вас взаимный лайк с {name}!").format(name=liker.name))
            except Exception as e:
                logger.warning(f"❌ Не удалось отправить liked_id взаимный лайк: {e}")

            try:
                if liked_img:
                    await bot.send_photo(
                        liker_id,
                        photo=liked_img,
                        caption=liked_profile_text,
                        reply_markup=mutual_like_markup,
                        parse_mode="HTML"
                    )
                else:
                    await bot.send_message(
                        liker_id,
                        liked_profile_text,
                        reply_markup=mutual_like_markup,
                        parse_mode="HTML"
                    )
            except Exception as e:
                logger.warning(f"❌ Не удалось отправить анкету liked_id={liked_id}: {e}")

            try:
                if liker_img:
                    await bot.send_photo(
                        liked_id,
                        photo=liker_img,
                        caption=liker_profile_text,
                        reply_markup=mutual_like_markup_for_liked,
                        parse_mode="HTML"
                    )
                else:
                    await bot.send_message(
                        liked_id,
                        liker_profile_text,
                        reply_markup=mutual_like_markup_for_liked,
                        parse_mode="HTML"
                    )
            except Exception as e:
                logger.warning(f"❌ Не удалось отправить анкету liker_id={liker_id}: {e}")

            liked_users.pop(liker_id, None)
            liked_users.pop(liked_id, None)

            try:
                await callback.message.delete()
            except Exception as e:
                logger.warning(f"Ошибка при удалении сообщения: {e}")

            return

        await bot.send_message(
            liked_id,
            __("✨ Вас лайкнули! Хотите посмотреть анкету?"),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=__("👀 Посмотреть анкету"), callback_data=f"view_{liker_id}")]
                ]
            )
        )

        try:
            await callback.message.edit_reply_markup(reply_markup=None)
        except Exception as e:
            logger.warning(f"Не удалось убрать кнопки после лайка: {e}")

        session_data = await state.get_data()
        liked_users_in_session = session_data.get("liked_users", set())
        liked_users_in_session.add(liked_id)
        await state.update_data(liked_users=liked_users_in_session)

    finally:
        if should_continue:
            await proceed_to_next_profile(state, callback)

