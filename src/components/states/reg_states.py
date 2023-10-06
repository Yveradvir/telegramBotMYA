from aiogram.dispatcher.filters.state import State, StatesGroup


class RegStates(StatesGroup):
    waitForNickname = State()
    waitForAge      = State()
    waitForCity     = State()
    waitForConf     = State()
    waitForDeleting = State()