import asyncio
import tgbot

from loader import (
    dp, storage, bot, ADMINS
)
    
async def main():
    try:
        for admin in ADMINS:
            await dp.bot.send_message(admin, "Бот Запущен")
            
        await dp.bot.set_my_commands(tgbot.utils.commands)
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())