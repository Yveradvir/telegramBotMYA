from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton)

def replyKeyboard(buttons, otk=True):
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(text=str(buttons[i])) for i in range(len(buttons))]
        ], resize_keyboard=True, one_time_keyboard=otk
    )
