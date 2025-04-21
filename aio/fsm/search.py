from aiogram.fsm.state import StatesGroup, State

class SearchState(StatesGroup):
    index = State()
    profiles = State()
