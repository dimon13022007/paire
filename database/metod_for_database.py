from .engine import async_sessions
from .models import RegisterUser, Lang, ReferalCode, UserReportTarget
from sqlalchemy import select, update, delete
import logging
from pydantic import BaseModel
from sqlalchemy import func
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Filter
from sqlalchemy import or_


logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")


likes_memory = {}
class MetodSQL:

    @staticmethod
    async def unieuq_add(data: BaseModel, object_class):
        try:
            async with async_sessions() as session:
                param_dict = data.model_dump()

                existing_entry = await session.execute(
                    select(object_class).where(object_class.user_name == param_dict["user_name"])
                )
                existing_entry = existing_entry.scalars().first()

                if existing_entry:
                    logging.warning(f"⚠️ Пользователь {param_dict['user_name']} уже существует! Обновляем данные...")

                    for key, value in param_dict.items():
                        setattr(existing_entry, key, value)

                    await session.commit()
                    return existing_entry

                new_entry = object_class(**param_dict)
                session.add(new_entry)
                await session.commit()
                logging.info(f"Новый пользователь добавлен: {param_dict['user_name']}")
                return new_entry

        except Exception as e:
            logging.error(f"Ошибка при добавлени или бля обновлении данных в {object_class.__name__}: {e}")
            return None

    @staticmethod
    async def add_filter(user_id, filter):
        async with async_sessions() as session:
            result = await session.execute(
                select(Filter).where(Filter.user_name == user_id)
            )
            existing_entry = result.scalars().first()

            if not existing_entry:
                new_filter = Filter(user_name=user_id, filter=filter)
                session.add(new_filter)
                await session.commit()
            elif existing_entry.filter != filter:
                existing_entry.filter = filter
                await session.commit()

    @staticmethod
    async def delete_filter(user_id):
        async with async_sessions() as session:
            result = await session.execute(
                select(Filter).where(Filter.user_name == user_id)
            )
            existing_entry = result.scalars().first()

            if existing_entry:
                existing_entry.filter = None
                await session.commit()


    @staticmethod
    async def see_filter(user_id):
        async with async_sessions() as session:
            stmt = await session.execute(
                select(Filter.filter).where(Filter.user_name==user_id)
            )
            res = stmt.scalars().first()
            return res

    @staticmethod
    async def get_language(user_id: int) -> str:
        async with async_sessions() as session:
            stmt = select(Lang.lang).filter_by(user_name=user_id)
            result = await session.execute(stmt)

            language = result.scalars().first()

            return language

    @staticmethod
    async def update_lang(user_id: int, new_lang: str):
        async with async_sessions() as session:
            try:
                result = await session.execute(
                    select(Lang).where(Lang.user_name == user_id)
                )

                user = result.scalars().first()

                if user:
                    user.lang = new_lang
                    await session.commit()
                    return True
                else:
                    logging.warning(f"Пользователь с ID {user_id} не найден.")
                    return False

            except Exception as e:
                await session.rollback()
                logging.error(f"Ошибка при обновлении языка: {e}")
                return False

    @staticmethod
    async def update_ref(user_id, field_name, new_value=None):
        async with async_sessions() as session:
            try:
                result = await session.execute(
                    select(ReferalCode).where(ReferalCode.user_name == user_id)
                )

                user = result.scalars().first()

                if not user:
                    return None

                if new_value is None:
                    return getattr(user, field_name, "🚫 Нет данных")

                if field_name == "img" and isinstance(new_value, bytes):
                    setattr(user, field_name, new_value)
                else:
                    setattr(user, field_name, new_value)

                await session.commit()
                return True

            except Exception as e:
                await session.rollback()
                logging.error(f"Ошибка при обновлении {field_name}: {e}")
                return None

    @staticmethod
    async def see_profile(user_name: int):
        result = None
        try:
            async with async_sessions() as session:
                query = await session.execute(
                    select(RegisterUser).filter(RegisterUser.user_name == user_name)
                )
                result = query.scalars().all()
        except Exception as err:
            print(f"Unexpected error: {repr(err)}")
        return result

    @staticmethod
    async def see_true(user_name: int) -> bool:
        try:
            async with async_sessions() as session:
                query = await session.execute(
                    select(RegisterUser).filter(RegisterUser.user_name == user_name)
                )
                result = query.scalars().first()
                return result is not None
        except Exception as err:
            print(f"Unexpected error: {repr(err)}")
            return False

    @staticmethod
    async def prim_key(user_id: int):
        async with async_sessions() as session:
            result = await session.execute(
                select(RegisterUser.user_name).where(RegisterUser.user_name == user_id)
            )
            primary_key = result.scalar()
            return primary_key

    @staticmethod
    async def user_id_code(user_id: int):
        async with async_sessions() as session:
            result = await session.execute(
                select(ReferalCode.code).where(ReferalCode.user_name == user_id)
            )
            res = result.scalar()
            return res

    @staticmethod
    async def user_code(user_code: str):
        async with async_sessions() as session:
            result = await session.execute(
                select(ReferalCode.user_name).where(ReferalCode.code == user_code)
            )
            res = result.scalar()
            return res

    @staticmethod
    async def count_ref(user_id: int):
        async with async_sessions() as session:
            result = await session.execute(
                select(ReferalCode.count).where(ReferalCode.user_name == user_id)
            )
            res = result.scalar()
            return res

    @staticmethod
    async def update_ref_count(user_id: int):
        async with async_sessions() as session:
            result = await session.execute(
                select(ReferalCode.count).where(ReferalCode.user_name == user_id)
            )
            current_count = result.scalar()

            if current_count == 1:
                return 1

            await session.execute(
                update(ReferalCode)
                .where(ReferalCode.user_name == user_id)
                .values(count=1)
            )
            await session.commit()
            return 1

    @staticmethod
    async def block_user(session: AsyncSession, user_id: int):
        await session.execute(
            update(RegisterUser)
            .where(RegisterUser.user_name == user_id)
            .values(is_blocked=True)
        )
        await session.commit()

    @staticmethod
    async def is_blocked(session: AsyncSession, user_id: int) -> bool:
        result = await session.execute(
            select(RegisterUser.is_blocked)
            .where(RegisterUser.user_name == user_id)
        )
        row = result.scalar()
        return bool(row)

    @staticmethod
    async def get_industry(user_id, num: int):
        async with async_sessions() as session:
            try:
                industry_fields = {
                    1: RegisterUser.industry,
                    2: RegisterUser.industry_1,
                    3: RegisterUser.industry_2
                }

                if num not in industry_fields:
                    return None

                field = industry_fields[num]

                result = await session.execute(
                    select(field).where(RegisterUser.user_name == user_id)
                )
                return result.scalars().first()

            except Exception as e:
                logging.error(f"❌ Помилка при отриманні industry #{num} для {user_id}: {e}")
                return None

    @staticmethod
    async def get_lang(user_id, num: int):
        async with async_sessions() as session:
            try:
                industry_fields = {
                    1: RegisterUser.language,
                    2: RegisterUser.language_2,
                }

                if num not in industry_fields:
                    return None

                field = industry_fields[num]

                result = await session.execute(
                    select(field).where(RegisterUser.user_name == user_id)
                )
                return result.scalars().first()

            except Exception as e:
                logging.error(f"❌ Помилка при отриманні industry #{num} для {user_id}: {e}")
                return None

    @staticmethod
    async def search_profiles(exclude_user_id: int = None, **filters) -> list[RegisterUser]:
        try:
            async with async_sessions() as session:
                query = select(RegisterUser).where(
                    RegisterUser.is_active == True,
                    RegisterUser.is_blocked == False
                )

                if exclude_user_id:
                    query = query.where(RegisterUser.user_name != exclude_user_id)

                industries_str = filters.get("industry", "").strip()
                if industries_str:
                    print(f"📥 Сировий фільтр по індустріях: {industries_str}")

                    industries = [industry.strip().lower() for industry in industries_str.split(",") if
                                  industry.strip()]
                    print(f"🔍 Відібрані індустрії: {industries}")

                    industry_conditions = []
                    for industry in industries:
                        print(f"🔗 Додаю умову для індустрії: {industry}")
                        industry_conditions.append(
                            or_(
                                func.lower(RegisterUser.industry).ilike(f"%{industry}%"),
                                func.lower(RegisterUser.industry_1).ilike(f"%{industry}%"),
                                func.lower(RegisterUser.industry_2).ilike(f"%{industry}%")
                            )
                        )

                    if industry_conditions:
                        query = query.where(or_(*industry_conditions))

                query = query.order_by(func.random())
                result = await session.execute(query)
                return result.scalars().all()

        except Exception as e:
            logging.error(f"Ошибка при поиске анкет: {e}")
            return []

    @staticmethod
    async def update(user_id, field_name, new_value=None):
        async with async_sessions() as session:
            try:
                result = await session.execute(
                    select(RegisterUser).where(RegisterUser.user_name == user_id)
                )

                user = result.scalars().first()

                if not user:
                    return None

                if new_value is None:
                    return getattr(user, field_name, "🚫 Нет данных")

                if field_name == "img" and isinstance(new_value, bytes):
                    setattr(user, field_name, new_value)
                else:
                    setattr(user, field_name, new_value)

                await session.commit()
                return True

            except Exception as e:
                await session.rollback()
                logging.error(f"Ошибка при обновлении {field_name}: {e}")
                return None

    @staticmethod
    async def update_none(user_id, field_name, new_value=None):
        async with async_sessions() as session:
            try:
                result = await session.execute(
                    select(RegisterUser).where(RegisterUser.user_name == user_id)
                )

                user = result.scalars().first()

                if not user:
                    return None

                if new_value is None and field_name in ["industry", "industry_1",
                                                        "industry_2"]:
                    if field_name == "industry":
                        return getattr(user, field_name)

                if field_name == "img" and isinstance(new_value, bytes):
                    setattr(user, field_name, new_value)
                else:
                    setattr(user, field_name, new_value)

                await session.commit()
                return True

            except Exception as e:
                await session.rollback()
                logging.error(f"Ошибка при обновлении {field_name}: {e}")
                return None

    @classmethod
    async def get_user_by_id(cls, user_id: int):
        async with async_sessions() as session:
            result = await session.execute(select(RegisterUser).filter(RegisterUser.user_name == user_id))
            return result.scalar()

    @staticmethod
    def add_like(liker_id: int, liked_id: int):
        likes_memory[(liker_id, liked_id)] = False

    @staticmethod
    def get_like(liker_id: int, liked_id: int):
        return likes_memory.get((liker_id, liked_id), False)

    @staticmethod
    async def unblock_user(session, user_id: int):
        await session.execute(
            update(RegisterUser)
            .where(RegisterUser.user_name == user_id)
            .values(is_blocked=False)
        )
        await session.commit()

    @staticmethod
    async def set_report_target(session: AsyncSession, user_id: int, target_id: int):
        await session.merge(UserReportTarget(user_id=user_id, target_id=target_id))
        await session.commit()

    @staticmethod
    async def get_report_target(session: AsyncSession, user_id: int) -> Optional[int]:
        result = await session.get(UserReportTarget, user_id)
        return result.target_id if result else None

    @staticmethod
    async def clear_report_target(session: AsyncSession, user_id: int):
        await session.execute(delete(UserReportTarget).where(UserReportTarget.user_id == user_id))
        await session.commit()

    @staticmethod
    def check_mutual_like(liker_id: int, liked_id: int):
        return likes_memory.get((liked_id, liker_id), False)

    @staticmethod
    def mark_mutual(liker_id: int, liked_id: int):
        if (liker_id, liked_id) in likes_memory and (liked_id, liker_id) in likes_memory:
            likes_memory[(liker_id, liked_id)] = True
            likes_memory[(liked_id, liker_id)] = True

    @staticmethod
    async def set_profile_active(user_id: int, is_active: bool):
        try:
            async with async_sessions() as session:
                result = await session.execute(
                    select(RegisterUser).where(RegisterUser.user_name == user_id)
                )
                user = result.scalar_one_or_none()
                if user:
                    user.is_active = is_active
                    await session.commit()
                else:
                    logging.warning(f"Пользователь {user_id} не найден")
        except Exception as e:
            logging.error(f"Ошибка при изменении активности профиля: {e}")



