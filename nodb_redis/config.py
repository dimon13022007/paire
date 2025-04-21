import redis.asyncio as redis
import asyncpg
import logging
import json
from database.config import settings
import asyncio

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.propagate = False

async def get_profile(redis_client):
    try:
        ttl = await redis_client.ttl("profile")
        if ttl and ttl > 10:
            logger.info(f"[REDIS] Кэш активен (TTL: {ttl}). Загружаем анкеты из Redis.")
            cached_profiles = await redis_client.get("profile")
            return json.loads(cached_profiles)

        logger.info("[REDIS] Кэш истек или отсутствует. Запрашиваем данные из PostgreSQL...")

        conn = await asyncpg.connect(
            user=settings.DB_USER,
            password=settings.DB_PASS,
            database=settings.DB_NAME,
            host=settings.DB_HOST,
            port=settings.DB_PORT
        )
        logger.info("✅ Подключено к PostgreSQL")

        rows = await conn.fetch("""
            SELECT id, user_name, city, name, age, text_disc, language, industry
            FROM register_user
            WHERE is_active = TRUE
            ORDER BY RANDOM()
            LIMIT 100
        """)

        rows_dicts = [dict(row) for row in rows]
        await redis_client.set("profile", json.dumps(rows_dicts), ex=60)
        logger.info(f"[REDIS] Кэш обновлен. Сохранено {len(rows_dicts)} анкет.")

        await conn.close()
        return rows_dicts

    except Exception as e:
        logger.error(f"Ошибка при работе с кэшем или БД: {e}")
        return []

if __name__ == '__main__':
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        decode_responses=True
    )

    profiles = asyncio.run(get_profile(redis_client))
    print("Анкеты из Redis/DB:", profiles)
