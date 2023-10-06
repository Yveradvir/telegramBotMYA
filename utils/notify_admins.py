from aiogram import Dispatcher
from config import ADMINS


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "[ 🎉 ]")
        except Exception as e:
            print(e)
            