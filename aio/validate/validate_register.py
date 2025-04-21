from aiogram.types import Message
from text_translete.translate import get_translator
import gettext
from database.metod_for_database import MetodSQL

class ValidateParam:
    @staticmethod
    async def validate_name(message: Message) -> bool:
        lang_param = await MetodSQL.get_language(message.from_user.id)
        print(lang_param)

        translator = await get_translator(lang_param)
        _ = translator.gettext
        if not message.text or not message.text[0].isupper():
            text = _("❌ Пожалуйста, имя должно начинаться с большой буквы")
            await message.answer(text)
            return False

        if len(message.text) < 2:
            text = _("❌ Пожалуйста, имя должно быть не меньше двух букв")
            await message.answer(text)
            return False

        if len(message.text) > 130:
            text = _("❌ Слишком длиное имя")
            await message.answer(text)
            return False

        if not message.text.isalpha():
            text = _("❌ Имя должно содержать только буквы.")
            await message.answer(text)
            return False

        return True

    @staticmethod
    async def validate_disc(message: Message):
        lang_param = await MetodSQL.get_language(message.from_user.id)
        print(lang_param)

        translator = await get_translator(lang_param)
        _ = translator.gettext

        if len(message.text) > 700:
            text = _("❌ Описание слишком длинное. Текст должен быть не больше 700 символов.")
            await message.answer(text)
            return False

        return True

    @staticmethod
    async def validate_city(message: Message):
        lang_param = await MetodSQL.get_language(message.from_user.id)
        print(lang_param)

        translator = await get_translator(lang_param)
        _ = translator.gettext

        if len(message.text) > 40:
            text = _("❌ Город не может в себе местить такое количество символов.")
            await message.answer(text)
            return False

        return True

    @staticmethod
    async def validate_language(message: Message):
        lang_param = await MetodSQL.get_language(message.from_user.id)
        print(lang_param)

        translator = await get_translator(lang_param)
        _ = translator.gettext

        if len(message.text) > 50:
            text = _("❌ Не существует языка программирования такой длинны.")
            await message.answer(text)
            return False
        return True

    @staticmethod
    async def validate_age(message: Message) -> bool:
        lang_param = await MetodSQL.get_language(message.from_user.id)
        print(lang_param)

        translator = await get_translator(lang_param)
        _ = translator.gettext
        if not message.text.isdigit():
            text = _("❌ Введите корректный возраст (только цифры).")
            await message.answer(text)
            return False

        age = int(message.text)
        if age <= 8 or age > 120:
            text = _("❌ Введите реальный возраст (8-120 лет).")
            await message.answer(text)
            return False

        if len(message.text) > 3:
            text = _("Вы ввели некорректный формат сообщения.")
            await message.answer(text)
            return False

        return True

    @staticmethod
    async def validate_photo(message: Message):
        lang_param = await MetodSQL.get_language(message.from_user.id)
        print(lang_param)

        translator = await get_translator(lang_param)
        _ = translator.gettext
        if not message.photo:
            text = _("Вы отправили не фото, пожалуйста, отправьте фото.")
            await message.answer(text)
            return False

        photo = message.photo[-1]
        if not photo or not isinstance(photo.file_id, str):
            text = _("Произошла ошибка при обработке фото, попробуйте снова.")
            await message.answer(text)
            return False

        return True

    @staticmethod
    async def validate_all(message: Message):
        lang_param = await MetodSQL.get_language(message.from_user.id)
        print(lang_param)

        translator = await get_translator(lang_param)
        _ = translator.gettext
        if len(message.text) > 50:
            text = _("Введен слишком длинный текст для данной категории")
            await message.answer(text)

            return False
        return True

