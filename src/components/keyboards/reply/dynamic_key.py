from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def this(buttons, otk = True):
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(text=buttons[iterable])
                for iterable in range(len(buttons))
            ]
        ], resize_keyboard=True, one_time_keyboard=otk
    )

