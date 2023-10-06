from aiogram.dispatcher.filters.state import State, StatesGroup


class PostStates(StatesGroup):
    waitForTitle    = State()
    waitForContent  = State()
    waitForOldMark  = State()
    waitForTag      = State()
    waitForFinal    = State()