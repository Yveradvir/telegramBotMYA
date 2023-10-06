from aiogram.dispatcher             import FSMContext
from loader                         import dp, db
from aiogram.types                  import Message

from src.components.keyboards.reply import dynamic_key

buttons = [
    ["[ ua ]"], ["[ us ]"]
]

help_ua = [
    "Команди:\n",
    "\t/reg - регестрація\n",
    "\t\t - нікнейм -> вік -> місце -> підтвердження\n",
    "\t/post - створення постів\n",
    "\t\t - титл -> опис -> вікова марка -> тег -> підтвердження\n",
    "\t/mypost - тут можна дізнатись про айді ваших постів для дій\n",
    "\t\t - минула сторінка -> вихід з режиму -> наступна сторінка\n",
    "\t/deactivation - деактівація\n",
]

help_en = [
    "Commands:\n",
    "\t/reg - Registration\n",
    "\t\t- nickname -> age -> location -> confirmation\n",
    "\t/post - Create posts\n",
    "\t\t- title -> description -> age rating -> tag -> confirmation\n",
    "\t/mypost - Check your post IDs for actions\n",
    "\t\t- previous page -> exit mode -> next page\n",
    "\t/deactivation - Deactivate your account\n",
]

@dp.message_handler(commands=["help"])
async def helping(message: Message):
    await message.answer("".join(help_en), reply_markup=dynamic_key.this(buttons[0]))

@dp.message_handler(text=buttons[0][0])
async def ua_help(message: Message):
    await message.answer("".join(help_ua), reply_markup=dynamic_key.this(buttons[1]))

@dp.message_handler(text=buttons[1][0])
async def helping(message: Message):
    await message.answer("".join(help_en), reply_markup=dynamic_key.this(buttons[0]))
