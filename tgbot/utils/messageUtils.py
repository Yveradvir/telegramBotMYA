import googletrans
from aiogram import types
from asyncio import sleep

async def warn(message: types.Message, text, timer = 2):
    warnMessage = await message.answer(text)
    await sleep(timer)
    await warnMessage.delete()

async def translateText(message: types.Message, text, lang):
    cursor = googletrans.Translator()
    cursor.translate()