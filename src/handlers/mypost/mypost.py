from loader                            import dp
from aiogram                           import types
from aiogram.dispatcher                import FSMContext

from src.components.states             import PostFindStates
from src.handlers.mypost.mypcomponents import (create_commissioner, err, 
                                               delete_commissioner, launch_data, 
                                               query_commissioner, hook_exists)

buttons = [
    ["[ < ]", "[ exit ]", "[ > ]"]
]


@dp.message_handler(commands=["mypost"])
async def mypost(message: types.Message, state: FSMContext):
    uid = message.from_user.id

    if await hook_exists(uid):
        async with state.proxy() as data:
            commissioner = await create_commissioner(message, buttons, "Okay, these is your posts")

            await PostFindStates.waitForExit.set() 
            await launch_data(data, uid, commissioner)

    else:
        await message.answer("Please, reg via /reg")


@dp.message_handler(content_types=types.ContentType.TEXT, state=PostFindStates.waitForExit)
async def handleForTheWait(message: types.Message, state: FSMContext):
    result = message.text

    async with state.proxy() as data:
        if result in buttons[0]:
            if result == buttons[0][1]:
                await dp.bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
                await delete_commissioner(data)
                await state.finish()
            else:
                if result == buttons[0][2]:     
                    if data["page"] <= len(data["posts"]) // 5: 
                        data["page"] += 1
                    else:
                        await err(message, f"sorry, but your page number is {data['page']}, more page not exists")
                
                elif result == buttons[0][0]:   
                    if data["page"] > 1:
                        data["page"] -= 1
                    else:
                        await err(message, "sorry, but your page number is 1, less page not exists")
                
                await dp.bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
                await delete_commissioner(data)
                await query_commissioner(message, buttons, data)
        