from getpass import getuser
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sql_db_tg import Register, Events, User, EditState, Picture, Pictures, WaitOffer, Item, Games, Economy, ItemState, \
    app, db
from datetime import datetime, timedelta
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.state import StateFilter
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app, session, Response
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F
from sqlalchemy.orm import sessionmaker
from admin_py import (admin_only)
import io
from aiogram.types import ContentType
from aiogram.types import InputFile
from io import BytesIO
import random
import logging
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
import tracemalloc
import os
from PIL import Image
import io
from aiogram.types import FSInputFile
import os

import pytz

from sqlalchemy import func

tracemalloc.start()

TOKEN = "7047369595:AAHvR_z5p9bxbOXR7yqxIW7uPpOnv26-jB4"
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

group_message_count = {}


def get_session():
    with app.app_context():
        Session = sessionmaker(bind=db.engine)
        return Session()


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    commands_list = (
        "/start - Начать работу с ботом\n"
        "/about - Информация о HardCore Affiliate Club\n"
        "/add_event - Добавить новое событие\n"
        "/events - Список ближайших событий\n"
        "/edit_event - Редактировать событие\n"
        "/delete_event - Удалить мероприятие\n"
        "/coins - Проверить количество монет\n"
        "/daily - Получить ежедневную награду\n"
        "/richest - Топ-10 самых богатых пользователей\n"
        "/coins_give - Передать монеты другому пользователю\n"
        "/economy - Просмотреть описание экономики\n"
        "/economy_edit - Редактировать описание экономики\n"
        "/games - Игры с ботом (кубики, камень-ножницы-бумага, рулетка, колесо фортуны)\n"
        "/games-edit - Редактировать описание игр\n"
        "/add_item - Добавить новый товар в магазин\n"
        "/edit_item - Редактировать товар\n"
        "/shop - Посмотреть товары в магазине\n"
        "/remove_item - Удалить товар из магазина\n"
        "/rps - Игра камень-ножницы-бумага\n"
        "/dice - Игра в кости\n"
        "/wheel - Колесо фортуны\n"
        "/buy_item - Купить товар в магазине\n"
        "/add_meme - Добавить новый мем\n"
        "/offer_meme - Предложить мем администратору\n"
        "/delete_meme - Удалить мем по ID"
    )
    await message.answer(commands_list)



@dp.message(Command("about"))
async def about_command(message: types.Message):
    await message.answer(
        text="😍 HardCore Affiliate Club (https://hardcoreclub.online/affiliateclub) — сообщество для разных участников сферы affiliate маркетинга. Не только вебов, ПП-шек и реклов, но и других, более \"теневых\" ролей. Сюда относятся все, кто работает в PR, HR, дизайне, контенте. Байеры, представители сервисов и технари. Продакты, проджекты и даже овнеры.\n\n"
             "Рынок сейчас такой, что один человек часто берет на себя сразу несколько функций. Льющий афф менеджер — это норма. Копирайтер становится PR-директором в ПП, а вебы пилят оффлайн-конфы не хуже опытных ивентщиков. Таких людей много, и всем им нужно место для безопасного нетворкинга.\n\n"
             "Такое место, где можно задать вопрос, закинуть идею — и тебе ответят, помогут, подскажут. Соберут войс для конструктивного обсуждения. А еще поболтают на отвлеченные темы типа котиков или пива. Но все это — с людьми, которые на все сто тебя понимают, потому что вы все работаете в одной сфере, и в любой момент можете переключиться на профитный рабочий контакт и партнерство.\n\n"
             "Наш слоган — \"нетворкинг в твоем ритме\". (https://hardcoreclub.online/affiliateclub) Мы регулярно собираемся в Discord, где нетворкаем, общаемся, играем в игры и проводим разные ивенты: как обучающие, так и развлекательные. Сформированные цели и видение помогают HardCore оставаться комфортным местом для всех. Например, на нашем сервере ты не найдешь скамеров или хантеров уровня \"привет бро видел тебя в чате есть сочный оффер\"."
    )


@dp.message(Command("add_event"))
async def add_event_start(message: types.Message, state: FSMContext):
    await message.answer("Укажите название мероприятия:")
    await state.set_state(Register.waiting_for_name)


@dp.message(StateFilter(Register.waiting_for_name))
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        "Укажите дату и время в формате [YYYY-MM-DD HH:MM] и часовой пояс по GMT в формате [-H или +H]"
    )
    await state.set_state(Register.waiting_for_time_event)


@dp.message(StateFilter(Register.waiting_for_time_event))
async def process_time_event(message: types.Message, state: FSMContext):
    try:
        input_text = message.text.strip()
        date_time_str, timezone_str = input_text.rsplit(" ", 1)
        event_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")

        if timezone_str.startswith("+") or timezone_str.startswith("-"):
            timezone_offset = int(timezone_str)
            timezone = pytz.FixedOffset(timezone_offset * 60)
        else:
            raise ValueError("Неверный формат часового пояса")

        event_time = pytz.utc.localize(event_time).astimezone(timezone)

        await state.update_data(time_event=event_time, timezone_offset=timezone_offset)

        await message.answer("Добавьте ссылку на пост-анонс мероприятия:")
        await state.set_state(Register.waiting_for_post_announcement_link)
    except ValueError:
        await message.answer(
            "Для создания мероприятия укажите дату и время в формате [YYYY-MM-DD HH:MM] и часовой пояс по GMT в формате [-H или +H]")
    except:
        await message.answer("Неизвестный часовой пояс. Попробуйте еще раз.")


@dp.message(StateFilter(Register.waiting_for_post_announcement_link))
async def process_post_announcement_link(message: types.Message, state: FSMContext):
    await state.update_data(post_announcement_link=message.text)
    await message.answer("Введите ссылку на Google Calendar:")
    await state.set_state(Register.waiting_for_google_calendar_link)


@dp.message(StateFilter(Register.waiting_for_google_calendar_link))
async def process_google_calendar_link(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_data["google_calendar_link"] = message.text

    new_event = Events(
        name=user_data["name"],
        time_event=user_data["time_event"],
        timezone_offset=user_data["timezone_offset"],
        post_announcement_link=user_data["post_announcement_link"],
        google_calendar_link=user_data["google_calendar_link"]
    )

    with app.app_context():
        try:
            db.session.add(new_event)
            db.session.commit()
            await message.answer(
                f"Мероприятие успешно создано и добавлено в базу!\n\n"
                f"ID мероприятия: {new_event.id}\n"
                f"Название: {new_event.name}\n"
                f"Время: {new_event.time_event.strftime('%Y-%m-%d %H:%M')} UTC{new_event.timezone_offset:+03d}\n"
                f"Ссылка на пост-анонс: {new_event.post_announcement_link}\n"
                f"Ссылка на Google Calendar: {new_event.google_calendar_link}"
            )

        except Exception as e:
            db.session.rollback()
            await message.answer(f"Произошла ошибка при добавлении в базу: {e}")

    await state.clear()


@dp.message(Command("events"))
async def add_event_start(message: types.Message, state: FSMContext):
    with app.app_context():
        try:
            current_time = datetime.now()

            nearest_event = Events.query.filter(Events.time_event > current_time) \
                .order_by(Events.time_event.asc()) \
                .limit(3).all()

            if nearest_event:
                await message.answer("Список ближайших мероприятий в HardCore Affiliate")
                response = ""
                num = 0
                for event in nearest_event:
                    num += 1
                    response += (
                        f"{num}\n"
                        f"ID мероприятия: {event.id or 'Нет'}\n"
                        f"📅 Название: {event.name}\n"
                        f"Время {event.time_event.strftime('%Y-%m-%d %H:%M')} {event.time_event.strftime('%z')}\n"
                        f"🔗 Пост-анонс: {event.post_announcement_link or 'Нет'}\n"
                        f"📌 Google Calendar: {event.google_calendar_link or 'Нет'}\n\n"

                    )
                await message.answer(response)
            else:
                await message.answer("Ближайших мероприятий пока нет.")
        except Exception as e:
            await message.answer(f"Произошла ошибка при получении данных: {e}")


@dp.message(Command("edit_event"))
async def edit_event_start(message: types.Message, state: FSMContext):
    await message.answer("Введите ID мероприятия, которое хотите редактировать:")
    await state.set_state("waiting_for_event_id")


@dp.message(StateFilter("waiting_for_event_id"))
async def process_event_id(message: types.Message, state: FSMContext):
    try:
        event_id = int(message.text)

        with app.app_context():
            event = Events.query.filter_by(id=event_id).first()

        if event:
            await state.update_data(event_id=event_id)
            await send_event_info(event, message, state)
        else:
            await message.answer("Мероприятие с указанным ID не найдено.")
            await state.finish()
    except ValueError:
        await message.answer("Неверный формат ID. Пожалуйста, введите числовой ID.")
        await state.finish()


def fetch_event(event_id, message, state):
    with current_app.app_context():
        event = Events.query.filter_by(id=event_id).first()

    if event:
        return send_event_info(event, message, state)
    else:
        return handle_event_not_found(message, state)


async def send_event_info(event, message, state):
    button = InlineKeyboardBuilder()
    button.button(text="Name", callback_data="Name")
    button.button(text="Date", callback_data="Date")
    button.button(text="Post-Anons", callback_data="Post-Anons")
    button.button(text="Google-Calendar", callback_data="Google-Calendar")
    button.adjust(1)

    await message.answer(f"Найдено мероприятие: {event.name}\n"
                         f"1. Название: {event.name}\n"
                         f"2. Время: {event.time_event} (Часовой пояс: {event.timezone_offset or 'Нет'})\n"
                         f"3. Пост-анонс: {event.post_announcement_link or 'Нет'}\n"
                         f"4. Google Calendar: {event.google_calendar_link or 'Нет'}\n"
                         "Какие изменения вы хотите внести?",
                         reply_markup=button.as_markup())


from datetime import datetime, timezone, timedelta




@dp.callback_query(F.data.in_({"Name", "Date", "Post-Anons", "Google-Calendar"}))
async def handle_field_edit(callback: types.CallbackQuery, state: FSMContext):
    field_mapping = {
        "Name": "name",
        "Date": "time_event",
        "Post-Anons": "post_announcement_link",
        "Google-Calendar": "google_calendar_link",
    }
    field = field_mapping.get(callback.data)

    if not field:
        await callback.message.answer("Ошибка: некорректное поле для изменения.")
        await callback.answer()
        return

    data = await state.get_data()
    event_id = data.get("event_id")

    with get_session() as session:
        event = session.query(Events).filter_by(id=event_id).first()
        if event:
            if field == "time_event":
                current_time = event.time_event or "Не определено"
                current_timezone = event.timezone_offset or "Не определено"
                await state.update_data(field=field)
                await callback.message.answer(
                    "Укажите дату, время и часовой пояс, покоторому проводится мероприятие."
                )
            else:
                current_value = getattr(event, field, "Не определено")
                await state.update_data(field=field)
                await callback.message.answer(
                    f"Введите новое значение для поля {field}.\n"
                    f"Текущее значение: {current_value}."
                )
            await state.set_state(EditState.waiting_for_new_value)
        else:
            await callback.message.answer("Мероприятие не найдено.")
    await callback.answer()


@dp.message(StateFilter(EditState.waiting_for_new_value))
async def save_new_value(message: types.Message, state: FSMContext):
    data = await state.get_data()
    field = data.get("field")
    event_id = data.get("event_id")

    with get_session() as session:
        event = session.query(Events).filter_by(id=event_id).first()
        if not event:
            await message.answer("Мероприятие не найдено.")
            await state.clear()
            return

        if field == "time_event":
            try:
                datetime_str, timezone_offset_str = map(str.strip, message.text.split(" +"))

                new_time_event = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

                timezone_offset = int(timezone_offset_str)
                new_time_event = new_time_event.replace(tzinfo=timezone(timedelta(hours=timezone_offset)))

                event.time_event = new_time_event
                event.timezone_offset = f"+{timezone_offset_str}"
                session.commit()

                await message.answer(f"Новое время: {new_time_event.strftime('%Y-%m-%d %H:%M %z')}\n"
                                     f"Новый часовой пояс: +{timezone_offset_str}")
            except ValueError:
                await message.answer(
                    "Ошибка: убедитесь, что формат соответствует 'ГГГГ-ММ-ДД ЧЧ:ММ +Часовой_пояс' (например, 2024-12-25 15:30 +2).")
        else:
            new_value = message.text.strip()
            setattr(event, field, new_value)
            session.commit()
            await message.answer(f"Новое значение для {field} сохранено: {new_value}")

    await state.clear()


@dp.message(Command("delete_event"))
async def delete_command(message: types.Message):
    try:

        if len(message.text.split()) < 2:
            await message.answer("Вы не ввели id команда должна быть такой /delete_event ID")
            return
        event_id = message.text.split()[1]

        if not event_id.isdigit():
            await message.answer("ID должен быть числом.")
            return

        event_id = int(event_id)

        with get_session() as session:
            event = session.query(Events).filter(Events.id == event_id).first()

            if event:
                session.delete(event)
                session.commit()
                await message.answer(f"Меропреятие удалено.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")


@dp.message(Command("coins"))
async def coins_count(message: types.Message):
    user_name = message.from_user.username

    if not user_name:
        await message.answer("У вас нет username в Telegram.")
        return

    with app.app_context():
        user = User.query.filter_by(name=user_name).first()
        if user:
            await message.answer(f"@{user.name} у тебя на счету {user.coins} HardCoins")
        else:
            await message.answer(
                f"Пользователь @{user_name} у тебя ничего нет! Введи команду /daily и получи награду!"
            )


base_reward = 100
serias = 2
bonus_coins = 777
max_serias = 10


def time_to_next_daily(last_daily_time):
    now = datetime.utcnow()
    next_daily_time = last_daily_time + timedelta(days=1)
    time_left = next_daily_time - datetime.utcnow()
    hours = time_left.seconds // 3600
    minutes = (time_left.seconds % 3600) // 60
    return f"{hours:02}:{minutes:02}"


@dp.message(Command("daily"))
async def daily(message: types.Message):
    session = get_session()
    user = session.query(User).filter_by(id=message.from_user.id, name=message.from_user.username).first()

    if not user:
        user = User(id=message.from_user.id, name=message.from_user.username)
        session.add(user)
        session.commit()

    now = datetime.utcnow()

    if user.last_daily:
        time_last_daily = now - user.last_daily
        if timedelta(hours=20) <= time_last_daily <= timedelta(hours=30):
            reward = base_reward * serias
            user.coins += reward
            user.serias_streak += 1

            if user.serias_streak >= max_serias:
                user.coins += bonus_coins
                await message.answer(
                    f"Поздравляем, ваша серия достигла максимальной длины {max_serias}! Вы получили бонус {bonus_coins} HardCoins.")
                user.serias_streak = 0
            else:
                await message.answer(
                    f"{reward} забирает ежедневную награду вместе с бонусом за {user.serias_streak} {bonus_coins} HardCoins.")
        else:
            time_left = time_to_next_daily(user.last_daily)
            await message.answer(
                f"@{message.from_user.username}, ты можешь использовать эту команду только раз в сутки. Потерпи еще {time_left}.")
    else:
        user.coins += base_reward
        user.serias_streak = 0
        await message.answer(f"{message.from_user.username} забирает ежедневную награду: {base_reward} HardCoins ")

    user.last_daily = now
    session.commit()


@dp.message(Command("richest"))
async def top_coins(message: types.Message):
    try:
        chat_name = message.chat.title if message.chat.title else message.chat.username
        with app.app_context():
            top_users = User.query.order_by(User.coins.desc()).limit(10).all()

        if top_users:
            top_message = f"Топ-10 самых богатых пользователей @{chat_name}:\n\n"
            for i, user in enumerate(top_users, 1):
                top_message += f"{i}. {user.name} - {user.coins} монет(ы)\n"

            await message.answer(top_message)
        else:
            await message.answer("Нет пользователей с монетами.")
    except Exception as e:
        await message.answer(f"Произошла ошибка при получении данных: {e}")


@dp.message(Command("coins_give"))
async def give_coins(message: types.Message):
    command_parts = message.text.split()

    if len(command_parts) != 3:
        await message.answer("Неправильная команда. /coins_give @username [coins]")
        return

    username = command_parts[1].replace('@', '')
    coins_amount = command_parts[2]

    try:
        coins_amount = int(coins_amount)
    except ValueError:
        await message.answer("Количество монет должно быть числом.")
        return

    session = get_session()
    user = session.query(User).filter_by(name=username).first()

    if user is None:
        await message.answer(f"Пользователь с username @{username} не найден.")
        return

    user.coins += coins_amount
    session.commit()

    await message.answer(
        f" @{message.from_user.username} перевел {coins_amount} HardCoins на счет @{username}.")


@dp.message(Command("economy"))
async def economy(message: types.Message):
    with app.app_context():
        economy_entry = db.session.query(Economy).first()

        if not economy_entry:
            new_entry = Economy(economy="Your economy text here")
            db.session.add(new_entry)
            db.session.commit()
            economy_entry = new_entry
            await message.answer("Новое сообщение добавлено.")
        else:
            await message.answer(f"{economy_entry.economy}")


@dp.message(Command("economy_edit"))
async def economy_edit(message: types.Message):
    command_parts = message.text.split(maxsplit=1)

    if len(command_parts) != 2:
        await message.answer("Неправильный формат команды: /economy_edit Новое сообщение")
        return

    new_description = command_parts[1]

    with app.app_context():
        economy_entry = db.session.query(Economy).first()

        if economy_entry:
            economy_entry.economy = new_description
            db.session.commit()
            await message.answer(f"Описание обновлено: {economy_entry.economy}")
        else:
            new_entry = Economy(economy=new_description)
            db.session.add(new_entry)
            db.session.commit()
            await message.answer(f"Новое описание создано: {new_entry.economy}")


@dp.message(Command("games"))
async def games(message: types.Message):
    with app.app_context():
        games_entry = db.session.query(Games).first()

        if not games_entry:
            new_entry = Games(
                games=(
                    "/dice <ставка> Брось два кубика так, чтобы набрать больше очков, чем бот. "
                    "Выбросишь две шестерки - получишь х3 от своей ставки. "
                    "/rps <ставка> «Камень, ножницы, бумага» против бота. "
                    "/roulette <ставка> Рулетка из шести шагов с повышением коэффициента на каждом шаге. "
                    "После успешного шага можешь забрать приз или поставить еще раз. "
                    "Дошел до конца – забрал джек-пот. "
                    "/wheel <ставка> Колесо фортуны! Можешь выиграть до +500 HardCoins или потерять столько же."
                )
            )
            db.session.add(new_entry)
            db.session.commit()
            games_entry = new_entry
            await message.answer("Новое сообщение добавлено.")
        else:
            await message.answer(f"{games_entry.games}")


@dp.message(Command("games-edit"))
async def games_edit(message: types.Message):
    command_parts = message.text.split(maxsplit=1)

    if len(command_parts) != 2:
        await message.answer("Неправильный формат команды: /games-edit Новое сообщение")
        return

    new_description = command_parts[1]

    with app.app_context():
        games_entry = db.session.query(Games).first()

        if games_entry:
            games_entry.games = new_description
            db.session.commit()
            await message.answer(f"Описание обновлено:\n\n {games_entry.games}")
        else:
            new_entry = Games(games=new_description)
            db.session.add(new_entry)
            db.session.commit()
            await message.answer(f"Новое описание создано:\n\n {new_entry.games}")


@dp.message(Command("add_item"))
async def add_item_start(message: types.Message, state: FSMContext):
    await message.answer("Укажите наименование товара.")
    await state.set_state(ItemState.waiting_for_name_good)


@dp.message(StateFilter(ItemState.waiting_for_name_good))
async def process_name_good(message: types.Message, state: FSMContext):
    await state.update_data(name_good=message.text)
    await message.answer("Укажите стоимость товара.")
    await state.set_state(ItemState.waiting_for_price_good)


@dp.message(StateFilter(ItemState.waiting_for_price_good))
async def process_price(message: types.Message, state: FSMContext):
    await state.update_data(price_good=message.text)
    await message.answer("Добавьте описание товара.")
    await state.set_state(ItemState.waiting_for_description_good)


@dp.message(StateFilter(ItemState.waiting_for_description_good))
async def process_desc(message: types.Message, state: FSMContext):
    await state.update_data(description_good=message.text)
    await message.answer("Загрузите изображение товара.")
    await state.set_state(ItemState.waiting_for_picture_good)


@dp.message(StateFilter(ItemState.waiting_for_picture_good), F.content_type == ContentType.PHOTO)
async def process_picture_db(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    file = await message.bot.get_file(file_id)
    photo_bytes = io.BytesIO()
    await message.bot.download_file(file.file_path, photo_bytes)
    photo_bytes.seek(0)

    await state.update_data(picture_good=photo_bytes.getvalue())
    user_data = await state.get_data()

    new_item = Item(
        name_good=user_data["name_good"],
        price_good=user_data["price_good"],
        description_good=user_data["description_good"],
        picture_good=user_data["picture_good"]
    )

    with app.app_context():
        try:
            db.session.add(new_item)
            db.session.commit()

            await message.answer(
                f"Товар добавлен\n\n"
                f"ID мероприятия: {new_item.id}\n"
                f"Название: {new_item.name_good}\n"
                f"Цена: {new_item.price_good}\n"
                f"Описание: {new_item.description_good}\n"
                f"Изображение сохранено:\n\n "
            )
        except Exception as e:
            await message.answer(f"Сталася помилка при додаванні товару: {str(e)}")
    await state.clear()


@dp.message(Command("edit_item"))
async def start_edit_item(message: types.Message, state: FSMContext):
    await message.answer("Введите ID товара, которое хотите редактировать:")
    await state.set_state("waiting_for_item_id")


@dp.message(StateFilter("waiting_for_item_id"))
async def process_item_id(message: types.Message, state: FSMContext):
    try:
        item_id = int(message.text)

        with app.app_context():
            item = Item.query.filter_by(id=item_id).first()

        if item:
            await state.update_data(item_id=item_id)
            await send_item_info(item, message, state)
        else:
            await message.answer("Товар с указанным ID не найден.")
            await state.finish()
    except ValueError:
        await message.answer("Неверный формат ID. Пожалуйста, введите числовой ID.")
        await state.finish()


def fetch_item(item_id, message, state):
    with current_app.app_context():
        item = Item.query.filter_by(id=item_id).first()

    if item:
        return send_item_info(item, message, state)
    else:
        return handle_item_not_found(message, state)


async def send_item_info(item, message, state):
    button = InlineKeyboardBuilder()
    button.button(text="Название", callback_data="Name_Good")
    button.button(text="Цена", callback_data="Price_Good")
    button.button(text="Описание", callback_data="Description")
    button.button(text="Фото", callback_data="Picture")
    button.adjust(1)

    await message.answer(
        f"Найден товар: {item.name_good}\n"
        f"1. Название: {item.name_good}\n"
        f"2. Цена: {item.price_good}\n"
        f"3. Описание: {item.description_good or 'Нет'}\n"
        "Какие изменения вы хотите внести?",
        reply_markup=button.as_markup()
    )


@dp.callback_query(F.data.in_({"Name_Good", "Price_Good", "Description", "Picture"}))
async def name_callback(callback: types.CallbackQuery, state: FSMContext):
    field_mapping = {
        "Name_Good": "name_good",
        "Price_Good": "price_good",
        "Description": "description_good",
        "Picture": "picture_good",
    }

    field = field_mapping.get(callback.data)
    if not field:
        await callback.message.answer("Ошибка: некорректное поле для изменения.")
        await callback.answer()
        return

    data = await state.get_data()
    item_id = data.get("item_id")

    print(f"ID товара: {item_id}, поле для изменения: {field}")

    with get_session() as session:
        item = session.query(Item).filter_by(id=item_id).first()
        if item:
            current_value = getattr(item, field, "Не определено")
            await state.update_data(field=field)
            await callback.message.answer(
                f"Введите новое значение текущее: {current_value}"
            )
            await state.set_state(ItemState.waiting_for_new_value_good)
        else:
            await callback.message.answer("Товар не найден.")
    await callback.answer()


@dp.message(ItemState.waiting_for_new_value_good)
async def update_item_field(message: types.Message, state: FSMContext):
    new_value = message.text
    data = await state.get_data()
    item_id = data.get("item_id")
    field = data.get("field")

    with get_session() as session:
        item = session.query(Item).filter_by(id=item_id).first()
        if item:
            setattr(item, field, new_value)
            session.commit()
            await message.answer(f"Значение '{field}' успешно обновлено на: {new_value}")
        else:
            await message.answer("Товар не найден.")
    await state.clear()


@dp.message(Command("shop"))
async def shop(message: types.Message):
    item_part = message.text.split()
    try:
        if len(item_part) < 2:
            try:
                with get_session() as session:
                    item = session.query(Item).all()

                    if not item:
                        await message.answer("Магазин пуст.")
                        return
                    response = ""
                    for items in item:
                        response += (f"Название: {items.name_good}\n"
                                     f"Цена: {items.price_good} HardCoins\n"
                                     f"ID Товара: {items.id}\n\n")

                    await message.answer(response)
            except Exception as e:
                await message.answer(f"Случилась ошибка: {str(e)}")

            finally:
                session.close()
        else:
            item_id = item_part[1]

            try:
                item_id = int(item_id)
            except ValueError:
                await message.answer("ID должно быть числом.")
                return

            with get_session() as session:
                item = session.query(Item).filter_by(id=item_id).first()

                if not item:
                    await message.answer(f"Товар с ID {item_id} не найден.")
                    return

                response = (
                    f"HardCore Affiliate Club Shop\n\n"
                    f"Описание предмета: {item.name_good}\n"
                    f"ID: {item.id}\n"
                    f"Стоимость: {item.price_good} HardCoins\n"
                    f"Описание:\n{item.description_good}\n"
                )

                await message.answer(response)
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")
        import traceback
        await message.answer(f"Трассировка ошибки:\n{traceback.format_exc()}")


@dp.message(Command("remove_item"))
async def delete_command(message: types.Message):
    try:

        if len(message.text.split()) < 2:
            await message.answer("Вы не ввели id команда должна быть такой /remove_item ID")
            return
        item_id = message.text.split()[1]

        if not item_id.isdigit():
            await message.answer("ID должен быть числом.")
            return

        item_id = int(item_id)

        with get_session() as session:
            item = session.query(Item).filter(Item.id == item_id).first()

            if item:
                session.delete(item)
                session.commit()
                await message.answer(f"Мероприятие с ID {item_id} успешно удалено.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")


@dp.message(Command("levels"))
async def top_level(message: types.Message):
    try:
        chat_name = message.chat.title if message.chat.title else message.chat.username
        chat_id = message.chat.id

        if chat_id not in group_message_count:
            await message.answer("Нет данных для этого чата.")
            return

        chat_users = group_message_count[chat_id]
        sorted_users = sorted(chat_users.items(), key=lambda x: x[1]['count'], reverse=True)

        top_message = f"HardCore Affiliate Club Leaderboard @{chat_name}:\n\n"

        with get_session() as session:
            for i, (user_id, data) in enumerate(sorted_users, 1):
                user = session.query(User).filter_by(id=user_id).first()
                if user:
                    level = get_level(user.experience)  # Calculate level for each user
                    top_message += f"{i}. {data['name']} - {data['count']} сообщений, уровень {level}\n"

        await message.answer(top_message)
    except Exception as e:
        await message.answer(f"Произошла ошибка при получении данных: {e}")


word = ["Камень", "Ножницы", "Бумага"]

def create_rps_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🪨 Камень", callback_data="rock"),
                InlineKeyboardButton(text="✂️ Ножницы", callback_data="scissors"),
                InlineKeyboardButton(text="📄 Бумага", callback_data="paper")
            ]
        ]
    )




@dp.message(Command("rps"))
async def start_rps(message: types.Message):
    with get_session() as session:
        user_id = message.from_user.id
        global bet
        print("Отправка кнопок...gdfghdfhdfhd")

        try:
            bet = int(message.text.split()[1])
        except (IndexError, ValueError):
            await message.answer("Укажите сумму ставки от 1 до 300 HardCoins. Пример: /rps 150")
            return

        user = session.query(User).get(user_id)
        print("Отпр")

        if user is None:
            await message.answer("У тебя ничего нету, перейди в команду /daily")
            return

        last_used = user.last_rps_use

        if last_used and datetime.now() - last_used < timedelta(days=1):
            await message.answer("Вы уже использовали эту команду в последние 24 часа. Попробуйте позже!")
            return
        print("Отправка кнопок")

        if bet < 1 or bet > 300:
            await message.answer("Ставка должна быть от 1 до 300 HardCoins!")
            return
        print("Отправка.")

        if user.coins < bet:
            await message.answer(
                f"{user.name}, у тебя не достаточно коинов")
            return

        print("Отправка кнопок...")
        await message.answer(f"Ставка {bet} HardCoins принята! Теперь выбирайте: камень, ножницы или бумага.",
                             reply_markup=create_rps_buttons())

        user.last_rps_use = datetime.now()
        session.commit()


@dp.callback_query(F.data == "rock")
async def rock(call: types.CallbackQuery):
    with get_session() as session:

        user = session.query(User).filter_by(id=call.from_user.id).first()

        bot_bit = random.choice(word)
        print(bot_bit)
        if "Камень" in bot_bit:
            await call.message.answer(
                f"@{call.message.from_user.username} выберает камень, я выбираю камень, это ничья, ты забирешь свою ставку {bet}")

        elif "Ножницы" in bot_bit:
            user_bet = bet * 2
            user.coins += user_bet
            session.commit()
            await call.message.answer(f"Камень побеждает ножницы ты выграл {user_bet}")

        elif "Бумага" in bot_bit:
            user.coins -= bet
            session.commit()
            await call.message.answer(f"Бумага побеждает камень, ты проиграл {bet}")


@dp.callback_query(F.data == "scissors")
async def rock(call: types.CallbackQuery):
    with get_session() as session:

        user = session.query(User).filter_by(id=call.from_user.id).first()

        bot_bit = random.choice(word)
        print(bot_bit)
        if "Камень" in bot_bit:
            user.coins -= bet
            session.commit()
            await call.message.answer(f"Камень побеждает ножницы, ты проиграл {bet}")

        elif "Ножницы" in bot_bit:
            await call.message.answer(
                f"@{call.message.from_user.username} выберает ножницы, я выбираю ножницы, это ничья, ты забирешь свою ставку {bet}")

        elif "Бумага" in bot_bit:
            user_bet = bet * 2
            user.coins += user_bet
            session.commit()
            await call.message.answer(f"Ножницы побеждают бумагу, ты выграл {user_bet}")


@dp.callback_query(F.data == "paper")
async def rock(call: types.CallbackQuery):
    with get_session() as session:

        user = session.query(User).filter_by(id=call.from_user.id).first()

        bot_bit = random.choice(word)
        print(bot_bit)

        if "Камень" in bot_bit:
            user_bet = bet * 2
            user.coins += user_bet
            session.commit()
            await call.message.answer(f"Бумага побеждает камень ты выграл {user_bet}")

        elif "Ножницы" in bot_bit:
            user.coins -= bet
            session.commit()
            await call.message.answer(f"Бумага проигрывает ножницам, ты проиграл {bet}")

        elif "Бумага" in bot_bit:
            await call.message.answer(
                f"@{call.message.from_user.username} выберает бумагу, я выбираю бумагу, это ничья, ты забирешь свою ставку {bet}")


chanell_id = -1002322279461


async def send_message(channel_id: int, text: str):
    await bot.send_message(channel_id, text)


@dp.message(Command("dice"))
async def start_dice(message: types.Message):
    with get_session() as session:
        user_id = message.from_user.id
        global bet1
        try:
            bet1 = int(message.text.split()[1])
        except (IndexError, ValueError):
            await message.answer("Укажите сумму ставки от 1 до 300 HardCoins. Пример: /dice 150")
            return

        user = session.query(User).get(user_id)

        if user is None:
            await message.answer("У тебя ничего нету, перейди сюда /daily")
            return

        if user.last_dice_use and (datetime.now() - user.last_dice_use) < timedelta(days=1):
            await message.answer("Вы уже использовали эту команду в последние 24 часа. Попробуйте позже!")
            return

        if bet1 < 1 or bet1 > 300:
            await message.answer("Ставка должна быть от 1 до 300 HardCoins!")
            return

        if user.coins < bet1:
            await message.answer(
                f"У вас недостаточно монет для ставки {bet1} HardCoins! У вас всего {user.coins} монет.")
            return

        dice_bot1 = random.randint(1, 6)
        dice_bot2 = random.randint(1, 6)

        dice_player1 = random.randint(1, 6)
        dice_player2 = random.randint(1, 6)

        total_bot = dice_bot1 + dice_bot2
        total_player = dice_player1 + dice_player2

        if total_bot > total_player:
            user.coins -= bet1
            result = f"@{message.from_user.username}, ты выбросил {dice_player1} и {dice_player2}, а я {dice_bot1} и {dice_bot2}. Ты проиграл."
        elif total_player > total_bot:
            betx2 = bet1 * 2
            user.coins += betx2
            result = f"@{message.from_user.username}, ты выбросил {dice_player1} и {dice_player2}, а я {dice_bot1} и {dice_bot2}. Ты выиграл, забирай {betx2} HardCoins."
        else:
            result = f"@{message.from_user.username}, ты выбросил {dice_player1} и {dice_player2}, и я выбросил {dice_bot1} и {dice_bot2}, это ничья, ты забираешь свою ставку {bet1} HardCoins."

        user.last_dice_use = datetime.now()
        session.commit()

        await message.answer(result)

def get_current_season():
    month = datetime.utcnow().month
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"


from datetime import datetime


def get_current_season():
    month = datetime.utcnow().month
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"


@dp.message(Command("buy"))
async def buy_item(message: types.Message):
    try:
        item_id = int(message.text.split()[1])
        user_id = message.from_user.id
        current_season = get_current_season()

        if len(message.text.split()) < 2:
            await message.answer("Вы не ввели id команда должна быть такой /buy_item ID")
            return

        with get_session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                await message.answer("Пользователь не найден.")
                return

            item = session.query(Item).filter_by(id=item_id).first()
            if not item:
                await message.answer("Товар не найден.")
                return

            if user.coins < item.price_good:
                await message.answer("У вас недостаточно монет для покупки этого товара.")
                return

            if user.season == current_season and user.item_id == item_id:
                await message.answer("Вы уже покупали этот товар в этом сезоне.")
                return
            level = get_level(user.experience)
            if level < 10:
                await message.answer("У вас еще не достаточно уровней для данной покупки")
            else:
                user.coins -= item.price_good
                user.season = current_season
                user.item_id = item_id
                user.timestamp = datetime.utcnow()
                session.delete(item)
                session.commit()

                await message.answer(
                    f"Вы успешно купили {item.name_good} за {item.price_good} монет!"
                )
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")


class RouletteGame(StatesGroup):
    in_game = State()


COEFFICIENTS = [1.1, 1.18, 1.38, 1.39, 1.6]
chanse = [0, 1]


@dp.message(Command("roulette"))
async def start_game(message: types.Message, state: FSMContext):
    try:
        with app.app_context():
            _, bet = message.text.split()
            bet = int(bet)

            user = User.query.filter_by(id=message.from_user.id).first()
            if not user:
                await message.answer("У тебя ничего нет. Введи команду /daily.")
                return

            if user.coins < bet:
                await message.answer("У вас недостаточно монет для ставки.")
                return

            if user.last_played and (datetime.now() - user.last_played) < timedelta(days=1):
                await message.answer("Вы можете играть только один раз в день. Попробуйте снова завтра.")
                return

            await state.update_data(bet=bet, round=0, current_win=bet, user_id=user.id)
            user.coins -= bet
            user.last_played = datetime.now()
            db.session.commit()

            await message.answer(
                f"@{message.from_user.username} ставит {bet} HardCoins и жмёт на спуск. Начинаем!",
                reply_markup=await generate_game_buttons()
            )

            await state.set_state(RouletteGame.in_game)
    except (ValueError, IndexError):
        await message.answer("Используйте формат: /roulette <ставка>")


async def generate_game_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Забрать", callback_data="take"),
                InlineKeyboardButton(text="Продолжить", callback_data="continue"),
            ]
        ]
    )


async def send_message_user(channel_id: int, text: str):
    await bot.send_message(channel_id, text)


async def send_message_user_markup(channel_id: int, text: str, markup):
    await bot.send_message(channel_id, text, reply_markup=markup)


@dp.callback_query(StateFilter(RouletteGame.in_game))
async def game_logic(callback_query: types.CallbackQuery, state: FSMContext):
    with app.app_context():
        user_data = await state.get_data()
        user = User.query.get(user_data["user_id"])

        if not user:
            await send_message_user(callback_query.message.chat.id, "Ошибка: Пользователь не найден.")
            await state.finish()
            return

        bet = user_data['bet']
        round_number = user_data['round']
        current_win = user_data['current_win']

        await callback_query.message.edit_reply_markup()

        if callback_query.data == "take":
            user.coins += current_win
            db.session.commit()

            await send_message_user(
                callback_query.message.chat.id,
                f"@{callback_query.from_user.username} забирает ставку {current_win} HardCoins. Игра завершена!"
            )
            await state.finish()
            return

        result = random.randint(0, 1)

        if result == 0:
            await send_message_user(
                callback_query.message.chat.id,
                f"@{callback_query.from_user.username} проиграл. Попробуй еще раз завтра."
            )
            await state.finish()
        else:
            round_number += 1
            if round_number > len(COEFFICIENTS):
                user.coins += current_win
                db.session.commit()

                await send_message_user(
                    callback_query.message.chat.id,
                    f"@{callback_query.from_user.username} выигрывает и забирает джек-пот {current_win} HardCoins!"
                )
                await state.finish()
                return

            current_win = int(current_win * COEFFICIENTS[round_number - 1])
            coefficient = COEFFICIENTS[round_number - 1]
            await state.update_data(round=round_number, current_win=current_win)

            await send_message_user_markup(
                callback_query.message.chat.id,
                f"Ты выиграл {current_win} HardCoins! Увеличиваешь ставку, чтобы выиграть ещё больше (коэффициент: x{coefficient})?",
                await generate_game_buttons()
            )


@dp.message(Command("wheel"))
async def fortune_wheel(message: types.Message):
    user_id = message.from_user.id
    cost = 150

    with get_session() as session:
        user = session.query(User).get(user_id)

        if user is None:
            await message.answer("У тебя ничего нету, перейди на команду /daily")
            return

        if user.coins < cost:
            await message.answer(f"У вас недостаточно монет для крутки! Стоимость одной крутки: {cost} HardCoins.")
            return

        last_used = user.last_wheel_use

        if last_used and datetime.now() - last_used < timedelta(days=1):
            await message.answer("Вы уже использовали команду колесо фортуны в последние 24 часа. Попробуйте позже!")
            return

        user.coins -= cost
        user.last_wheel_use = datetime.now()
        session.commit()

    msg = await message.answer(f"@{message.from_user.username} раскручивает колесо фортуны!")

    await asyncio.sleep(random.randint(3, 5))
    res = [0,-1,-10,-100,-250,-500,1,10,100,250,500]

    result = random.choice(res)

    if result < 0:
        result_text = f"@{message.from_user.username} {result}. В следующий раз повезет!"
    else:
        result_text = f"@{message.from_user.username} {result}. Сегодня удача на твоей стороне, может и с аппрувом повезет."

    await msg.edit_text(result_text)


@dp.message(Command("add_meme"))
async def add_item_start(message: types.Message, state: FSMContext):
    await message.answer("Отправте мем который хотите добавить.")
    await state.set_state(Pictures.waiting_for_pict)


@dp.message(StateFilter(Pictures.waiting_for_pict), F.content_type == ContentType.PHOTO)
async def process_picture_db(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    file = await message.bot.get_file(file_id)
    photo_bytes = io.BytesIO()
    await message.bot.download_file(file.file_path, photo_bytes)
    photo_bytes.seek(0)

    await state.update_data(picture=photo_bytes.getvalue())
    user_data = await state.get_data()

    new_item = Picture(
        picture=user_data["picture"]
    )

    with app.app_context():
        try:
            db.session.add(new_item)
            db.session.commit()

            await message.answer(
                f"ID {new_item.id}\n"
                f"Мем сохранен: "
            )
        except Exception as e:
            await message.answer(f"Ошибка: {str(e)}")
    await state.clear()

@dp.message(Command("offer_meme"))
async def offer(message: types.Message, state: FSMContext):
    await message.answer("Отправьте ваше предложение")
    await state.set_state(WaitOffer.waiting_for_offer)


async def send_admin(chat_ids, photo, caption=None):
    for chat_id in chat_ids:
        await bot.send_photo(chat_id, photo=photo, caption=caption)


@dp.message(StateFilter(WaitOffer.waiting_for_offer), F.content_type == ContentType.PHOTO)
async def meme_offer(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    admin = [998279547,5148825065,7009934641]

    await send_admin(admin, photo, caption="Новое предложение мема!")
    await message.answer("Ваше предложение отправлено!")
    await state.clear()


@dp.message(Command("delete_meme"))
async def delete_command(message: types.Message):
    try:

        if len(message.text.split()) < 2:
            await message.answer("Вы не ввели id команда должна быть такой /delete_meme meme_ID")
            return
        meme_id = message.text.split()[1]

        if not meme_id.isdigit():
            await message.answer("ID должен быть числом.")
            return

        meme_id = int(meme_id)

        with get_session() as session:
            meme = session.query(Picture).filter(Picture.id == meme_id).first()

            if meme:
                session.delete(meme)
                session.commit()
                await message.answer(f"Мем с ID {meme_id} успешно удалено.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")


IMAGE_FOLDER = 'static/images'
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

IMGUR_CLIENT_ID = '6f2534e59278fc1'


async def upload_image_to_imgur(image_data):
    url = "https://api.imgur.com/3/upload"
    headers = {
        "Authorization": f"Client-ID {IMGUR_CLIENT_ID}"
    }
    files = {
        'image': image_data
    }
    response = requests.post(url, headers=headers, files=files)
    if response.status_code == 200:
        data = response.json()
        return data['data']['link']
    else:
        return None


async def send_random_picture(message: types.Message):
    try:
        with app.app_context():
            random_picture = Picture.query.order_by(func.random()).first()
            if random_picture:
                temp_file_path = os.path.join(IMAGE_FOLDER, f"{random_picture.id}.jpg")
                with open(temp_file_path, 'wb') as temp_file:
                    temp_file.write(random_picture.picture)

                photo = FSInputFile(temp_file_path)
                await message.answer_photo(photo, caption=f"Мем дня для {message.from_user.username}")
            else:
                await message.answer("Нет сохраненных мемов в базе данных.")
    except Exception as e:
        await message.answer(f"Ошибка при получении изображения: {str(e)}")
        
@dp.message(Command("meme"))
async def meme_command(message: types.Message):
    await send_random_picture(message)


def get_level(experience):
    level_thresholds = [
        (100, 1),
        (250, 2),
        (500, 3),
        (750, 4),
        (1000, 5),
        (1500, 6),
        (2250, 7),
        (3250, 8),
        (4500, 9),
        (6000, 10),
        (7750, 11),
        (9750, 12),
        (12000, 13),
        (14600, 14),
        (17550, 15),
        (20850, 16),
        (24500, 17),
        (28500, 18),
        (32850, 19),
        (37550, 20)
    ]
    for threshold, level in level_thresholds:
        if experience < threshold:
            return level - 1
    return 20


@dp.message()
async def count_messages(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.username

    if chat_id not in group_message_count:
        group_message_count[chat_id] = {}

    if user_id in group_message_count[chat_id]:
        group_message_count[chat_id][user_id]['count'] += 1
    else:
        group_message_count[chat_id][user_id] = {
            'count': 1,
            'name': user_name
        }

    with get_session() as session:
        user = session.query(User).filter_by(id=user_id).first()

        if not user:
            user = User(
                id=user_id,
                name=message.from_user.username,
                coins=0,
                experience=0,
                last_message_time=None,
                message_count=0
            )
            session.add(user)
            session.commit()

        if user.last_message_time and (datetime.utcnow() - user.last_message_time) < timedelta(minutes=1):
            return

        experience_gained = random.randint(15, 25)
        user.experience += experience_gained
        user.last_message_time = datetime.utcnow()  # Update last message time
        session.commit()


async def handle_event_not_found(message, state):
    await message.answer("Событие не найдено.")
    await state.finish()


async def handle_item_not_found(message, state):
    await message.answer("Товар не найдено.")
    await state.finish()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
