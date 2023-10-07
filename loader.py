import config

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

storage = MemoryStorage()
bot     = Bot(token=config.BOT_TOKEN, parse_mode='HTML')
dp      = Dispatcher(bot, storage=storage)

