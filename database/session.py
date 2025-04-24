import ssl
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String
from typing import Annotated
from database.config import settings


BASE_DIR = Path(__file__).resolve().parent.parent
CA_PATH = BASE_DIR / "ca_certificat" / "ca-certificate.crt"


ssl_context = ssl.create_default_context(cafile=str(CA_PATH))

# 🔌 Создание движка
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
async_session = async_sessions