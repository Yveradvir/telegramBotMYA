from loader                            import db, dp, Render
from asyncio                           import sleep
from aiogram                           import types

from src.components.keyboards.reply    import dynamic_key

render = Render()

async def hook_exists(uid):
    return await db.hook_exists(uid)

async def create_commissioner(message: types.Message, buttons, text):
    return await message.answer(text,
                                reply_markup=dynamic_key.this(buttons[0], otk=False))
            
async def launch_data(data, uid, commissioner):
    data["id"]                  = uid
    data["page"]                = 0
    data["posts"]               = await render._quering_mypost(await db.return_all_my_post(uid))
    data["commissioner_id"]     = commissioner.message_id 
    data["commissioner_chat"]   = commissioner.chat.id

async def delete_commissioner(data):
    await dp.bot.delete_message(message_id=data["commissioner_id"],
                                chat_id=data["commissioner_chat"])
    
async def err(message: types.Message, text):
    err = await message.answer(text)
    await sleep(3)
    await dp.bot.delete_message(chat_id=err.chat.id, message_id=err.message_id)
    
async def query_commissioner(message: types.Message, buttons, data):
    quering = await render.query_mypost(data["posts"])

    res = await create_commissioner(message,
                                    buttons, 
                                    await render.page(quering[data["page"]]))
    data["commissioner_id"] = res.message_id
