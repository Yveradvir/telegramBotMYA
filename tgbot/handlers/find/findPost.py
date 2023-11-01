from tgbot import keyboards, utils
from tgbot.states import PostStates
from loader import dp, db
from aiogram import types
from aiogram.dispatcher import FSMContext
from random import randint

buttons = ["🆔", "🎫"]
callback = ["id", "translate"]

async def random_post(message: types.Message, state, post_id):
    async with db as slot:
        async with state.proxy() as data:
            currentPost = (await slot.isExistsPost(post_id, True))[0]
            
            if currentPost:
                data["profile_id"] = post_id
                try:
                    data["language"] = (await slot.isExists(message.from_user.id))[0]['language']
                except Exception:
                    return "Sorry, you aren't exist"
                else:
                    msg = f''
                    msg += f'ℹ {str(currentPost["name"])}\n'
                    
                    return msg

@dp.message_handler(commands=["findps"])
async def findps(message: types.Message, state: FSMContext):
    async with db as slot:
        currentUser = (await slot.isExists(message.from_user.id))[0]
        if currentUser and currentUser != []:
            try:
                post_id = randint(1, await slot.allTableCount("users"))
                result = await random_post(message, state, post_id)
                await message.answer(
                    text=result,
                    reply_markup=keyboards.inlineKeyboard(buttons, callback)
                )
            except Exception as e:
                print(e)
                await utils.transWarn(
                    message, "Вибачте, але щось сталося",
                    currentUser["language"]
                ) 
        else:
            await utils.warn(
                message, "Sorry, but you are not exist",
            )
