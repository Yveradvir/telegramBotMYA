import asyncio
import logging
import tgbot

from loader import (
    dp, storage, bot
)
    

async def main():
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())