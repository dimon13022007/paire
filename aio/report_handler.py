from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from database.metod_for_database import MetodSQL
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aio.bot_token import bot
from database.session import async_session
from aio.services.match_service import proceed_to_next_profile, logger

router = Router()

ADMIN_ID = 826039504

@router.callback_query(F.data.startswith("report_"))
async def report_callback(callback: CallbackQuery, state: FSMContext):
    reporter_id = callback.from_user.id
    reported_id = int(callback.data.split("_")[1])

    await callback.message.answer("🚨 Жалоба отправлена!")

    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception as e:
        logger.warning(f"Не удалось удалить кнопки после жалобы: {e}")

    try:
        reported_user = await MetodSQL.get_user_by_id(reported_id)
    except Exception as e:
        logger.error(f"Не удалось получить анкету пользователя {reported_id}: {e}")
        await bot.send_message(ADMIN_ID, f"🚨 Жалоба на ID {reported_id}, но не удалось загрузить анкету.")
        return

    profile_text = f"<b>{reported_user.city}</b>\n" \
                   f"{reported_user.name} ({reported_user.age})\n" \
                   f"{reported_user.industry} | {reported_user.language}"

    if reported_user.text_disc:
        profile_text += f"\n\n{reported_user.text_disc}"

    complaint_text = (
        f"🚨 <b>Жалоба на пользователя</b>\n"
        f"👤 <b>ID анкеты:</b> <code>{reported_id}</code>\n"
        f"📩 <b>От пользователя:</b> <code>{reporter_id}</code>\n\n"
        f"<b>Анкета:</b>\n{profile_text}\n\n"
        f"<i>Заблокировать?</i>"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🚫 Заблокировать", callback_data=f"block_{reported_id}"),
            InlineKeyboardButton(text="🔓 Разблокировать", callback_data=f"unblock_{reported_id}")
        ]
    ])

    if reported_user.img:
        photo = BufferedInputFile(reported_user.img, filename="reported.jpg")
        await bot.send_photo(chat_id=ADMIN_ID, photo=photo, caption=complaint_text, reply_markup=kb, parse_mode="HTML")
    else:
        await bot.send_message(chat_id=ADMIN_ID, text=complaint_text, parse_mode="HTML", reply_markup=kb)

    await proceed_to_next_profile(state, callback)


@router.callback_query(F.data.startswith("block_"))
async def block_callback(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[1])

    async with async_session() as session:
        await MetodSQL.block_user(session, user_id)

    await callback.answer("✅ Пользователь заблокирован")
    await callback.message.edit_text(f"🔒 Пользователь {user_id} заблокирован.")

@router.callback_query(F.data.startswith("unblock_"))
async def unblock_callback(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[1])

    async with async_session() as session:
        await MetodSQL.unblock_user(session, user_id)

    await callback.answer("✅ Пользователь разблокирован")
    await callback.message.edit_text(f"🔓 Пользователь {user_id} разблокирован.")