from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class Photo(StatesGroup):
    ON_GET_PHOTO = State()
    ON_GET_ADDRESS = State()
    ON_GET_FIO = State()


class AdminSettings(StatesGroup):
    WAITING_FOR_WELCOME_TEXT = State()
    WAITING_FOR_WELCOME_LINK = State()
    WAITING_FOR_LINK_TEXT = State()
