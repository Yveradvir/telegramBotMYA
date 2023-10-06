from aiogram.dispatcher.filters.state import State, StatesGroup


class PostFindStates(StatesGroup):
    waitForExit = State()