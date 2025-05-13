from .engine import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import LargeBinary, BigInteger, JSON
from sqlalchemy import Boolean
from typing import Optional


class UserReportTarget(Base):
    __tablename__ = "user_report_target"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    target_id: Mapped[int] = mapped_column(BigInteger)

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
    language_2: Mapped[Optional[str]]
    industry: Mapped[str]
    industry_1: Mapped[Optional[str]]
    industry_2: Mapped[Optional[str]]
    img: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)

class  Filter(Base):
    __tablename__ = "filter"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[int] = mapped_column(BigInteger, unique=True)
    filter: Mapped[str] = mapped_column(nullable=True)


class Advertisement(Base):
    __tablename__ = "advertisement"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    image_path: Mapped[Optional[str]] = mapped_column(nullable=True)

