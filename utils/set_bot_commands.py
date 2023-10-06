from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Start bot"),
            types.BotCommand("help", "Help"),
            types.BotCommand("reg", "register your account"),
            types.BotCommand("post", "Make a post"),
            types.BotCommand("mypost", "Your post"),
            types.BotCommand("deactivation", "delete your account")
        ]
    )
