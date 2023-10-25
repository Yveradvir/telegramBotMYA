from aiogram.dispatcher.filters.state import State, StatesGroup

class RegStates(StatesGroup):
    waitForName = State()
    waitForAge = State()
    waitForDescription = State()
    waitForLanguage = State()
    waitForProfile = State()
    waitForConfirm = State()
    waitForRemove = State()