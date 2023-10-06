from config                             import *
from src.db                             import tools
from src.db.render                      import Render
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram                            import Bot, Dispatcher, types

bot     = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp      = Dispatcher(bot, storage=storage)
db      = tools.Database()
render  = Render()