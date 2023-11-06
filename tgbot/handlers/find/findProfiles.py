from tgbot import keyboards, utils
from loader import dp, db
from aiogram import types
from aiogram.dispatcher import FSMContext
from random import randint

buttons = ["🆔 author", "🎫 translate"]
callback = ["id", "translate"]

async def random_profile(message: types.Message, state: FSMContext, profile_id):
    async with db as slot:
        async with state.proxy() as data:
            currentProfile = (await slot.isExists(profile_id, True))[0]
            
            if currentProfile:
                data["profile_id"] = profile_id
                try:
                    cruser = (await slot.isExists(message.from_user.id))[0]
                    data["language"] = cruser['language']
                except Exception:
                    return "Sorry, you aren't exist"
                else:
                    if currentProfile['profile'] == True and currentProfile['tid']:
                        chatofuser = await dp.bot.get_chat(currentProfile['tid'])
                        use = chatofuser.username

                    else: use = "N/A"
                    msg = f''
                    msg += f'ℹ name - {str(currentProfile["name"])}\n'
                    msg += f'ℹ age  - {str(currentProfile["age"])}\n'
                    msg += f'ℹ descriprion - {str(currentProfile["description"])}\n'
                    msg += f'ℹ language    - {str(currentProfile["language"])}\n'
                    msg += f'ℹ username    - {use}'

                    return msg

@dp.callback_query_handler(text=callback[0])
async def getProfId(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await utils.transWarn(message, f'ID цього запису -> \n{data["profile_id"]}', data["language"], timer=6)

@dp.callback_query_handler(text=callback[1])
async def getProfTrans(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        async with db as slot:
            profile = await utils.justTrans((await slot.isExists(data["profile_id"], True))[0]["description"], data["language"])
            await utils.transWarn(message, f'Переклад цього запису -> \n{profile}', data["language"], timer=6)

@dp.message_handler(commands=["findpr"])
async def findp(message: types.Message, state: FSMContext):
    async with db as slot:
        currentUser = (await slot.isExists(message.from_user.id))[0]
        if currentUser and currentUser != []:
            try:
                profile_id = randint(1, await slot.allTableCount("users"))
                result = await random_profile(message, state, profile_id)
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

@dp.message_handler(commands=["findprid"])
async def findpId(message: types.Message, state: FSMContext):
    async with db as slot:
        try:
            currentUser = (await slot.isExists(message.from_user.id))[0]
        except Exception as e:
            print(e)
            await utils.warn(message, "Sorry, something is wrong. Maybe you aren't exist")
        else:
            try:
                parts = message.text.split()
                if len(parts) >= 2:
                    profile_id = int(parts[1])
                    result = await random_profile(message, state, profile_id)
                    await message.answer(text=result, reply_markup=keyboards.inlineKeyboard(buttons, callback))
                else:
                    await utils.transWarn(
                        message, "Sorry, but you didn't provide an ID. Send this command like \"/findprid <ID>\"",
                        currentUser['language']
                    )
            except KeyError:
                await utils.transWarn(
                    message, "Sorry, something went wrong. Please check your input.",
                    currentUser['language']
                )
