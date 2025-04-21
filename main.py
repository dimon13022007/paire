import asyncio
import redis.asyncio as redis
from database.config import settings
from database.create_tables import create_table
from aio.handlers.start_handlers.start import main_context
from nodb_redis.config import get_profile
from aio.state.session_memory import auto_clear_memory, auto_clear_dislikes_only
import logging
import sys


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout
)
logging.getLogger().setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("✅ Логгер настроен и работает")


async def main():
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        decode_responses=True
    )

    profiles_task = asyncio.create_task(get_profile(redis_client))
    clear_memory_task = asyncio.create_task(auto_clear_memory())
    create_table_task = asyncio.create_task(create_table())
    main_context_task = asyncio.create_task(main_context())
    clear_dislikes_task = asyncio.create_task(auto_clear_dislikes_only())

    profiles = await profiles_task
    logger.info(f"Fetched profiles: {profiles}")

    await create_table_task
    await main_context_task
    await clear_dislikes_task
    await clear_memory_task


if __name__ == "__main__":
    asyncio.run(main())







