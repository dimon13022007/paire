from aiogram.fsm.state import StatesGroup, State

class AdInputState(StatesGroup):
    text = State()
    image = State()
