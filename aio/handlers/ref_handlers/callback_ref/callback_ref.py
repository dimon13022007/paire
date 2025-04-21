from aiogram.types import CallbackQuery
from aiogram import Router, F
import random
from database.models import ReferalCode
import string
from pydantic_schemas.unique_param import ParamCode
from database.metod_for_database import MetodSQL
from text_translete.translate import get_translator
import gettext
from aio.handlers.ref_handlers.ref_keyboards.keyboard_for_ref import RefKeyboards

router = Router()

def generate_random_string(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


@router.callback_query(F.data == "code")
async def callback_ref(callback: CallbackQuery):
    await callback.answer("")

    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext
    user_id = callback.from_user.id

    if await MetodSQL.user_id_code(user_id):
        code = await MetodSQL.user_id_code(user_id)
        print(code)
        text = _("🎉 <b>Вы уже получили свой реферальный код!</b>\n\n"
                 "<code>{code}</code>\n\n"
                 "🔹 Поделитесь им с друзьями, чтобы получить бонусы! 😉").format(code=code)
        await callback.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=await RefKeyboards.ref_key(user_id)
        )
        return

    rand = generate_random_string(10)
    user = callback.from_user.id
    print(rand)
    print(user)
    user_code = f"{rand}{user}"
    print(user_code)

    await MetodSQL.unieuq_add(ParamCode(user_name=callback.from_user.id, code=user_code), object_class=ReferalCode)

    text = _("🎁 <b>Вот твой реферальный код!</b>\n\n"
             "<code>{user_code}</code>\n\n"
             "🔹 Отправь его друзьям, чтобы получить бонусы! 🚀").format(user_code=user_code)
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=await RefKeyboards.ref_key(user_id)

    )











