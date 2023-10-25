from tgbot              import keyboards, utils
from tgbot.states       import PostStates
from loader             import dp, db

from aiogram            import types
from aiogram.dispatcher import FSMContext

from random import randint

async def random_profile(message: types.Message, profile_id):
    await message.answer(profile_id)

@dp.message_handler(commands=["findpr"])
async def findp(message: types.Message, state: FSMContext):
    async with db as slot:
        currentUser = (await slot.isExists(message.from_user.id))[0]
        print(currentUser["age"])
        if currentUser and currentUser != []:
            try:
                await random_profile(message, randint(1, await slot.allTableCount("users")))
            except Exception as e:
                print(e)
                await utils.transWarn(
                    message, "Вибачте, але щось сталося",
                    currentUser["language"]
                ) 
        else:
            await utils.transWarn(
                    message, "Sorry, but you are not exist",
                    currentUser["language"]
                )
@dp.message_handler(commands=["findprId"])
async def findpId(message: types.Message, state: FSMContext):
    pass