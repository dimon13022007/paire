from aiogram.fsm.state import State, StatesGroup

class FSMReport(StatesGroup):
    reason = State()
    custom_reason = State()

class FSMWarning(StatesGroup):
    input_text = State()
    confirm = State()