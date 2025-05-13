from aiogram.fsm.state import StatesGroup, State

class IndustryState(StatesGroup):
    waiting_for_industry_choice = State()

class LangState(StatesGroup):
    waiting_for_lang_choice = State()

