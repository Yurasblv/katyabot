from aiogram.dispatcher.filters.state import State, StatesGroup


class Person(StatesGroup):
    ACCEPT = State()
    PERSON_CREDS = State()
    AGE = State()
    HEIGHT = State()
    WEIGHT = State()
    GOAL = State()
    LOCATION = State()
    EQUIPMENT_BOOLEAN = State()
    EQUIPMENT_INFO = State()
    CONTRAINDICATIONS_BOOLEAN = State()
    CONTRAINDICATIONS_INFO = State()
    BREAST_SIZE = State()
    WAIST_SIZE = State()
    HIPS_SIZE = State()
