from src.handlers           import * 
from loader                 import dp
from aiogram                import executor
from src.components         import middlewares
from utils.notify_admins    import on_startup_notify
from utils.set_bot_commands import set_default_commands

async def on_startup(dispatcher):
    try:
        await set_default_commands(dispatcher)
        await on_startup_notify(dispatcher)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    dp.middleware.setup(middlewares.MidExists())
    executor.start_polling(dp, on_startup=on_startup)
