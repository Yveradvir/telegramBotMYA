import googletrans
from aiogram import types
from asyncio import sleep

async def warn(message: types.Message, text, timer = 7):
    warnMessage = await message.answer(text)
    await sleep(timer)
    await warnMessage.delete()

async def justTrans(text, lang):
    cursor = googletrans.Translator()
    transtext = cursor.translate(text=text, dest=lang)
    return transtext.text

async def transWarn(message: types.Message,
                    text:str, lang:str, 
                    markup=None, timer: float = 7):
    
    cursor = googletrans.Translator()
    transtext = cursor.translate(text=text, dest=lang)
    if markup is None:
        warnMessage = await message.answer(text=transtext.text)
        await sleep(timer)
        await warnMessage.delete()
    else:
        warnMessage =await message.answer(text=transtext.text, reply_markup=markup)
        await sleep(timer)
        await warnMessage.delete()


async def translateText(message: types.Message, text, lang, markup=None):
    cursor = googletrans.Translator()
    transtext = cursor.translate(text=text, dest=lang)
    if markup is None:
        await message.answer(text=transtext.text)
    else:
        await message.answer(text=transtext.text, reply_markup=markup)
    