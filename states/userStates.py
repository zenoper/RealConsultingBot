from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    fullname = State()
    date_of_birth = State()
    interORlocal = State()
    phone_number = State()
    phone_number_int = State()
    grade = State()
    degree = State()
    test_score = State()
    confirmation = State()


class GradeStates(StatesGroup):
    school = State()
    university = State()


class TestStates(StatesGroup):
    ielts = State()
    duolingo = State()


class B1orF1States(StatesGroup):
    start = State()
    B1 = State()
    F1 = State()


class B1UserState(StatesGroup):
    abroad = State()
    countries = State()