from database.metod_for_database import MetodSQL
import io
from aiogram.types import  BufferedInputFile
from aiogram import Bot
import logging
from text_translete.translate import get_translator
import gettext


async def profile(bot: Bot, user: int, chat_id: int, reply_mark=None):
    lang_param = await MetodSQL.get_language(user)
    print(lang_param)

    translator = await get_translator(lang_param)
    _ = translator.gettext
    profiles = await MetodSQL.see_profile(user)
    print("Reply markup:", reply_mark)

    if profiles:
        for profile in profiles:
            img_bytes = io.BytesIO(profile.img)
            img_bytes.seek(0)
            img_file = BufferedInputFile(img_bytes.read(), filename="profile.jpg")

            def escape_md2(text: str) -> str:
                if text:
                    return text.translate(str.maketrans({
                        '_': r'\_',#ChatGPT
                        '*': r'\*',#ChatGPT
                        '[': r'\[',#ChatGPT
                        ']': r'\]',#ChatGPT
                        '(': r'\(',#ChatGPT
                        ')': r'\)',#ChatGPT
                        '~': r'\~',#ChatGPT
                        '`': r'\`',#ChatGPT
                        '>': r'\>',#ChatGPT
                        '#': r'\#',#ChatGPT
                        '+': r'\+',#ChatGPT
                        '-': r'\-',#ChatGPT
                        '=': r'\=',#ChatGPT
                        '|': r'\|',#ChatGPT
                        '{': r'\{',#ChatGPT
                        '}': r'\}',#ChatGPT
                        '.': r'\.',#ChatGPT
                        '!': r'\!'#ChatGPT
                    }))
                return ""

            caption_text = _(
                "📍 Город: {city}\n"
                "👤 Имя: {name}\n"
                "🎂 Возраст: {age}\n"
                "📝 Описание: {desc}\n"
                "💻 Язык: {lang}\n"
                "💼 Отрасль: {industry}"
            ).format(
                city=escape_md2(profile.city),
                name=escape_md2(profile.name),
                age=profile.age,
                desc=escape_md2(profile.text_disc),
                lang=escape_md2(profile.language),
                industry=escape_md2(profile.industry)
            )

            caption_text_none = _(
                "📍 Город: {city}\n"
                "👤 Имя: {name}\n"
                "🎂 Возраст: {age}\n"
                "💻 Язык: {lang}\n"
                "💼 Отрасль: {industry}"
            ).format(
                city=escape_md2(profile.city),
                name=escape_md2(profile.name),
                age=profile.age,
                lang=escape_md2(profile.language),
                industry=escape_md2(profile.industry)
            )

            if not profile.text_disc:
                await bot.send_photo(
                    chat_id=chat_id,
                    photo=img_file,
                    caption=caption_text_none,
                    parse_mode="MarkdownV2",
                    reply_markup=reply_mark
                )
            else:
                await bot.send_photo(
                    chat_id=chat_id,
                    photo=img_file,
                    caption=caption_text,
                    parse_mode="MarkdownV2",
                    reply_markup=reply_mark
                )




