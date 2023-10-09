import asyncio
import logging
import tgbot

from loader import (
    dp, storage, bot, config 
)
    

async def main():
    try:
        for admin in config.ADMINS:
            await dp.bot.send_message(admin, "Бот Запущен")

        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())