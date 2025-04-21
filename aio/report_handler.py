from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from aio.bot_token import bot
from database.metod_for_database import MetodSQL
from aio.services.match_service import send_profile_with_buttons, logger, proceed_to_next_profile
from database.session import async_session
from types import SimpleNamespace
from aio.context.states_and_config import FSMReport, FSMWarning

router = Router()

ADMIN_ID = 826039504


@router.callback_query(F.data.startswith("report_"))
async def report_callback(callback: CallbackQuery, state: FSMContext):
    reporter_id = callback.from_user.id
    reported_id = int(callback.data.split("_")[1])
    async with async_session() as session:
        await MetodSQL.set_report_target(session, reporter_id, reported_id)

    data = await state.get_data()
    await state.update_data(
        report_source_msg=callback.message,
        profiles=data.get("profiles"),
        index=data.get("index", 0)
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗣 Неприемлемый контент", callback_data="r_reason_content")],
        [InlineKeyboardButton(text="🤬 Оскорбления", callback_data="r_reason_abuse")],
        [InlineKeyboardButton(text="👻 Фейковый профиль", callback_data="r_reason_fake")],
        [InlineKeyboardButton(text="✏️ Другое", callback_data="r_reason_other")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="cancel_report")],
    ])
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("🚨 Укажите причину жалобы:", reply_markup=kb)
    await state.set_state(FSMReport.reason)


@router.callback_query(F.data == "cancel_report")
async def cancel_report(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(None)
    async with async_session() as session:
        await MetodSQL.clear_report_target(session, callback.from_user.id)
    await callback.message.edit_reply_markup(reply_markup=None)

    if "profiles" in data and "index" in data:
        profiles = data["profiles"]
        index = data["index"]
        if index < len(profiles):
            await send_profile_with_buttons(callback.from_user.id, profiles[index], index)
            return

    await callback.message.answer("Анкеты закончились")


@router.callback_query(F.data.startswith("r_reason_"))
async def report_reason_handler(callback: CallbackQuery, state: FSMContext):
    reporter_id = callback.from_user.id
    reason_code = callback.data.split("_")[2]

    reasons = {
        "content": "Неприемлемый контент",
        "abuse": "Оскорбления",
        "fake": "Фейковый профиль",
        "other": "Другое"
    }

    reason_text = reasons.get(reason_code, "Не указано")
    await state.update_data(reason=reason_text)

    if reason_code == "other":
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer("✏️ Напишите свою причину жалобы текстом:")
        await state.set_state(FSMReport.custom_reason)
    else:
        await callback.message.edit_reply_markup(reply_markup=None)
        await send_complaint_to_admin(callback, state)


@router.message(FSMReport.custom_reason)
async def custom_reason_input(message: Message, state: FSMContext):
    await state.update_data(reason=message.text)
    await send_complaint_to_admin(message, state)


async def send_complaint_to_admin(source_msg, state: FSMContext):
    reporter_id = source_msg.from_user.id
    data = await state.get_data()
    reason = data.get("reason")
    async with async_session() as session:
        reported_id = await MetodSQL.get_report_target(session, reporter_id)

    source_for_next = data.get("report_source_msg")

    try:
        await bot.send_message(reporter_id, "✅ Ваша жалоба отправлена на рассмотрение.")
    except Exception as e:
        logger.warning(f"Не удалось отправить подтверждение жалобы: {e}")

    try:
        reported_user = await MetodSQL.get_user_by_id(reported_id)
    except Exception as e:
        logger.error(f"Не удалось получить анкету пользователя {reported_id}: {e}")
        await bot.send_message(ADMIN_ID, f"🚨 Жалоба на ID {reported_id}, но не удалось загрузить анкету.")
        return

    profile_text = f"<b>{reported_user.city}</b>\n{reported_user.name} ({reported_user.age})\n{reported_user.industry} | {reported_user.language}"
    if reported_user.text_disc:
        profile_text += f"\n\n{reported_user.text_disc}"

    complaint_text = (
        f"🚨 <b>Жалоба на пользователя</b>\n"
        f"👤 <b>ID анкеты:</b> <code>{reported_id}</code>\n"
        f"📩 <b>От пользователя:</b> <code>{reporter_id}</code>\n"
        f"📄 <b>Причина:</b> {reason}\n\n"
        f"<b>Анкета:</b>\n{profile_text}\n\n"
        f"<i>Выберите действие:</i>"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🚫 Заблокировать", callback_data=f"block_{reported_id}"),
            InlineKeyboardButton(text="🔓 Разблокировать", callback_data=f"unblock_{reported_id}"),
            InlineKeyboardButton(text="⚠️ Предупреждение", callback_data=f"warn_{reported_id}")
        ]
    ])

    if reported_user.img:
        photo = BufferedInputFile(reported_user.img, filename="reported.jpg")
        await bot.send_photo(chat_id=ADMIN_ID, photo=photo, caption=complaint_text, reply_markup=kb, parse_mode="HTML")
    else:
        await bot.send_message(chat_id=ADMIN_ID, text=complaint_text, reply_markup=kb, parse_mode="HTML")

    if source_for_next:
        dummy_callback = CallbackQuery(
            id="dummy",
            from_user=source_msg.from_user,
            chat_instance="dummy_chat",
            message=source_for_next,
            data=None
        )
        await proceed_to_next_profile(state, dummy_callback)

    await state.set_state(None)
    async with async_session() as session:
        await MetodSQL.clear_report_target(session, source_msg.from_user.id)


@router.callback_query(F.data.startswith("block_"))
async def block_user(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[1])
    try:
        async with async_session() as session:
            await MetodSQL.block_user(session, user_id)
        await callback.answer("✅ Пользователь заблокирован")
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔓 Разблокировать", callback_data=f"unblock_{user_id}")]
        ])
        await callback.message.edit_reply_markup(reply_markup=kb)
    except Exception as e:
        logger.error(f"❌ Ошибка при блокировке пользователя {user_id}: {e}")
        await callback.answer("Произошла ошибка при блокировке ❌", show_alert=True)


@router.callback_query(F.data.startswith("unblock_"))
async def unblock_user(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[1])
    try:
        async with async_session() as session:
            await MetodSQL.unblock_user(session, user_id)
        await callback.answer("✅ Пользователь разблокирован")
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🚫 Заблокировать", callback_data=f"block_{user_id}"),
                InlineKeyboardButton(text="🔓 Разблокировать", callback_data=f"unblock_{user_id}"),
                InlineKeyboardButton(text="⚠️ Предупреждение", callback_data=f"warn_{user_id}")
            ]
        ])
        await callback.message.edit_reply_markup(reply_markup=kb)
    except Exception as e:
        logger.error(f"❌ Ошибка при разблокировке пользователя {user_id}: {e}")
        await callback.answer("Ошибка при разблокировке ❌", show_alert=True)


@router.callback_query(F.data.startswith("warn_"))
async def warn_user_start(callback: CallbackQuery, state: FSMContext):
    warned_id = int(callback.data.split("_")[1])
    await state.set_state(FSMWarning.input_text)
    await state.update_data(target_user=warned_id)
    await callback.message.answer("✏️ Введите причину предупреждения")


@router.message(FSMWarning.input_text)
async def warn_user_text(message: Message, state: FSMContext):
    await state.update_data(warning_text=message.text)
    await state.set_state(FSMWarning.confirm)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_warn"),
            InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_warn")
        ]
    ])
    await message.answer(f"Вы уверены, что хотите отправить предупреждение с текстом:\n\n{message.text}",
                         reply_markup=kb)


@router.callback_query(F.data == "confirm_warn")
async def confirm_warn(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("target_user")
    reason = data.get("warning_text")
    await bot.send_message(user_id, f"⚠️ Вы получили предупреждение от администрации:\n\nПричина: {reason}")
    await callback.message.edit_text("✅ Предупреждение отправлено")
    await state.clear()


@router.callback_query(F.data == "cancel_warn")
async def cancel_warn(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("❌ Отменено")
    await state.clear()
