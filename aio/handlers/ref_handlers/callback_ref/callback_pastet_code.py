from aiogram import Router, F
from database.metod_for_database import MetodSQL
from aiogram.types import CallbackQuery, Message
from aio.context.ref_code.context_ref import RefContext
from aiogram.fsm.context import FSMContext
from aio.bot_token import bot
from aio.func.func_profile import profile
from aio.keyboards.keyboard_for_restart_register import ChangeRegister
from text_translete.translate import get_translator
import gettext
from aio.handlers.ref_handlers.ref_keyboards.keyboard_for_ref import RefKeyboards


router = Router()

@router.callback_query(F.data == "code2")
async def paste_code(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")

    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext
    text = _("Введите ваш реферальный код")
    await callback.message.answer(text)
    await state.set_state(RefContext.waiting_for_code)

@router.message(RefContext.waiting_for_code)
async def waiting_for_code(message: Message):
    lang_param = await MetodSQL.get_language(message.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext
    ref_code = message.text
    user_id = message.from_user.id
    user = int(user_id)

    print(f"{ref_code} ref code")

    res = await MetodSQL.user_code(ref_code)

    if res:
        checked = await MetodSQL.user_id_code(message.from_user.id)
        if checked == ref_code:
            text = _("Вы ввели свой же код😅")
            await message.answer(text
)
            return

        count = await MetodSQL.count_ref(message.from_user.id)
        if count == 1:
            text = _("Ты уже вводил реферальный код\n\n"
                     "<i>Прости, но его можно вводить только один раз 🫠</i>")
            await message.answer(
                text,
                parse_mode="HTML"
            )
            await profile(bot, user, message.chat.id, reply_mark=await ChangeRegister.changed_register(message.from_user.id))
            return

        chat_id = res
        text = _("Вашу реферальную ссылку использовали\n\n"
                 "<i>Пользователь: @{username}! 🥳</i>\n\n"
                 "Теперь вас ждет <b>буст к вашей анкете</b>!").format(username=message.from_user.username)

        await bot.send_message(
            chat_id,
            text,
            parse_mode="HTML"
        )
        await MetodSQL.update_ref_count(user_id)
        text = _("Код принят!")
        await message.answer(text)

        await profile(bot, user, message.chat.id, reply_mark=await ChangeRegister.changed_register(message.from_user.id))
    else:
        text = _("Не наебывай меня {username}, даже не пытайся наебать").format(username=message.from_user.username)
        await message.answer(text)

