from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    waiting_for_full_name = State()
    waiting_for_sber_id = State()
    waiting_for_team_number = State()
    waiting_for_role_number = State()
    waiting_for_level_number = State()
    waiting_for_activity_description = State()
