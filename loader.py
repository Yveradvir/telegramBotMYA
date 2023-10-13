from config import *

from tgbot.utils import Database
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot     = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp      = Dispatcher(bot, storage=storage)
db      = Database()    