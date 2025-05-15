from .engine import async_engine
from .engine import Base


async def create_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
 
