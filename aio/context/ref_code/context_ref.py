from aiogram.fsm.state import StatesGroup, State

class RefContext(StatesGroup):
    waiting_for_code = State()

