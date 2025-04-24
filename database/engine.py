import ssl
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from .config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import Annotated
from sqlalchemy import String


ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False,
    connect_args={"ssl": ssl_context}
)

async_sessions = async_sessionmaker(async_engine, expire_on_commit=False)

async def get_async_session() -> AsyncSession:
    async with async_sessions() as session:
        yield session

str_256 = Annotated[str, 256]

class Base(DeclarativeBase):
    type_anotation_map = {
        str_256: String(256)
    }
