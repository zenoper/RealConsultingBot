from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    fullname = State()
    date_of_birth = State()
    phone_number = State()
    grade = State()
    degree = State()
    test_score = State()
    confirmation = State()
    waiting = State()

class GradeStates(StatesGroup):
    school = State()
    university = State()

class TestStates(StatesGroup):
    ielts = State()
    duolingo = State()