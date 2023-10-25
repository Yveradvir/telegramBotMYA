from aiogram import types

async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "start"),
        types.BotCommand("reg", "Register and re-register"),
        types.BotCommand("npost", "new post"),
        types.BotCommand("deactivarion", "deactivate your account"),
    ])