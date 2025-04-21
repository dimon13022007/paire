from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram import F
from aio.handlers.routers.router_for_start import router
from database.metod_for_database import MetodSQL
from aio.bot_token import bot
import io
from text_translete.translate import get_translator
import gettext


@router.callback_query(F.data.startswith("view_"))
async def view_profile_callback(callback: CallbackQuery, state: FSMContext):
    lang_param = await MetodSQL.get_language(callback.from_user.id)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext
    viewer_id = callback.from_user.id
    liked_id = int(callback.data.split("_")[1])

    liker_profile = await MetodSQL.get_user_by_id(liked_id)

    if liker_profile:
        if liker_profile.text_disc == None:
            profile_text = (
                f"{liker_profile.name} ({liker_profile.age})\n"
                f"{liker_profile.industry} | {liker_profile.language}, {liker_profile.city}"
            )
        else:
            profile_text = (
                f"{liker_profile.name} ({liker_profile.age})\n"
                f"{liker_profile.industry} | {liker_profile.language}, {liker_profile.text_disc}, {liker_profile.city}"
            )


        buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👍", callback_data=f"like_{liked_id}"),
             InlineKeyboardButton(text="👎", callback_data="skips")]
        ])

        if liker_profile.img:
            image_stream = io.BytesIO(liker_profile.img)
            image_stream.seek(0)
            img_file = BufferedInputFile(image_stream.read(), filename="profile.jpg")
            await bot.send_photo(chat_id=viewer_id, photo=img_file, caption=profile_text, reply_markup=buttons, parse_mode="HTML")
        else:
            await bot.send_message(viewer_id, profile_text, reply_markup=buttons, parse_mode="HTML")

        await callback.message.delete()
    else:
        text = _("Ошибка: профиль не найден!")
        await callback.answer(text, show_alert=True)
