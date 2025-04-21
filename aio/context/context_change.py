from aiogram.fsm.state import StatesGroup, State

class ChangeRegisterParam(StatesGroup):
    city = State()
    name = State()
    age = State()
    text_disc = State()
    language = State()
    industry = State()
    img = State()

class ChangeLocation(StatesGroup):
    city = State()
