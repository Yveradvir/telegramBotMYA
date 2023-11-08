from aiogram import types, Bot


commands = [
    types.BotCommand("start", "start"),
    types.BotCommand("help", "help"),
    types.BotCommand("reg", "Register and re-register"),
    types.BotCommand("npost", "new post"),
    types.BotCommand("deactivation", "deactivate your account"),
    types.BotCommand("findpr", "You get a random profile"),
    types.BotCommand("findps", "You get a random post"),
    types.BotCommand("findprid", "You get a profile by id, if exists"),
    types.BotCommand("findpsid", "You get a post by id, if exists")
]