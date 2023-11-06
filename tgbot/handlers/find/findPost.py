from tgbot import keyboards, utils
from loader import dp, db
from aiogram import types
from aiogram.dispatcher import FSMContext
from random import randint

buttons = ["🆔 author", "🎫 translate", "⚓ anwser id"]
callback = ["postauthorid", "posttranslate", "postaid"]

async def random_post(message: types.Message, state, post_id):
    async with db as slot:
        async with state.proxy() as data:
            currentPost = (await slot.isExistsPost(post_id))[0]

            if currentPost:
                data["post_id"] = post_id
                if currentPost['answer_id'] is not None:
                    data["answer_id"] = currentPost['answer_id']
                else: data['answer_id'] = "Цей пост не відповідає на інші пости"
                try:
                    data["language"] = (await slot.isExists(message.from_user.id))[0]['language']
                except Exception:
                    return "Sorry, you aren't exist"
                else:

                    msg = f''
                    msg += f'ℹ {str(currentPost["title"])}\n'
                    msg += f'ℹ {str(currentPost["content"])}\n'

                    return msg

@dp.callback_query_handler(text=callback[0])
async def getPostId(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await utils.transWarn(message, f'ID цього запису -> \n{data["post_id"]}', data["language"], timer=6)


@dp.callback_query_handler(text=callback[1])
async def getPostTrans(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        async with db as slot:
            post = await utils.justTrans(( await slot.isExistsPost(data["post_id"]))[0]["content"], data["language"])
            await utils.transWarn(message, f'Переклад цього запису -> \n{post}', data["language"], timer=6)

@dp.callback_query_handler(text=callback[2])
async def getPostAId(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        async with db as slot:
            await utils.transWarn(message, f'AID цього запису -> \n{data["answer_id"]}', data["language"], timer=6)

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

@dp.message_handler(commands=["findpsid"])
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
                print(parts)
                if len(parts) >= 2:
                    post_id = int(parts[1])
                    result = await random_post(message, state, post_id)
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
