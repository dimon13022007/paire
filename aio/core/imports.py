from aiogram.filters.command import Command, Message
from aiogram.fsm.context import FSMContext
from aio.keyboards.keyboard_for_start import MetodKeyboardInline
from database.metod_for_database import MetodSQL
from aio.context.context_fsm import RegisterState, CityRegister
from aio.handlers.routers.routers import dp
from aio.bot_token import bot
import asyncio
from aio.handlers.routers.router_for_start import router
from aiogram.types import ReplyKeyboardRemove, BufferedInputFile, CallbackQuery, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram import F
from aio.func.func_profile import profile
from aio.keyboards.keyboard_for_restart_register import ChangeRegister
from database.models import RegisterUser
from pydantic_schemas.unique_param import Param, ParamCity, ParamLarge
from aiogram.types import FSInputFile
import io
import logging
from cachetools import TTLCache
from aiogram.fsm.state import StatesGroup, State
import random
from aiogram import types
from aiogram.exceptions import TelegramAPIError
from cachetools import TTLCache



