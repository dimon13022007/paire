from .engine import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import LargeBinary, BigInteger
from typing import Optional
from sqlalchemy import Boolean



class ReferalCode(Base):
    __tablename__ = "refcode"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[int] = mapped_column(BigInteger)
    code: Mapped[str]
    count: Mapped[Optional[int]] = mapped_column(default=0)

class Lang(Base):
    __tablename__ = "lang"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[int] = mapped_column(BigInteger)
    lang: Mapped[str]


class RegisterUser(Base):
    __tablename__ = "register_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[int] = mapped_column(BigInteger, unique=True)
    city: Mapped[str]
    name: Mapped[str]
    age: Mapped[str]
    text_disc: Mapped[Optional[str]]
    language: Mapped[str]
    industry: Mapped[str]
    img: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)

class Advertisement(Base):
    __tablename__ = "advertisement"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    image_path: Mapped[Optional[str]] = mapped_column(nullable=True)

