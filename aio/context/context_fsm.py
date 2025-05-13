from aiogram.fsm.state import StatesGroup, State

class RegisterState(StatesGroup):
    name = State()
    age = State()
    text_disc = State()
    language = State()
    industry = State()
    industry_1 = State()
    industry_2 = State()
    industry_page = State()
    img = State()

class CityRegister(StatesGroup):
    city = State()



