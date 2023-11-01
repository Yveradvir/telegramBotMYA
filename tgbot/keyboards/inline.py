from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def inlineKeyboard(text_button, callback_text):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text_button[i],
            callback_data=callback_text[i]) for i in range(len(text_button))]
        ]
    )