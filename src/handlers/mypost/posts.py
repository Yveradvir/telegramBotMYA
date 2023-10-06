from loader                            import dp, db
from aiogram                           import types
from aiogram.dispatcher                import FSMContext

from src.components.states             import PostStates
from src.components.keyboards.reply    import dynamic_key

buttons = [
    ["[ I don't want to write content for post. ]"],
    ["[ Post for ages > 18 y.o ]", "[ Post for all ages ]"],
    ["[ My post is not have a tag ]"],
    [
        "[ Confrime [ 🚀 ] ]",
        "[ Decline  [ 🛑 ] ]"
    ]
]

@dp.message_handler(commands=["post"])
async def post(message: types.Message, state: FSMContext):
    uid = message.from_user.id

    if await db.hook_exists(uid):
        async with state.proxy() as data:
            data["id"] = uid

            await PostStates.waitForTitle.set()
            await message.answer("Let's share our feelings, enter title [ no more that 40 characters ]")

@dp.message_handler(content_types=[types.ContentType.TEXT], state=PostStates.waitForTitle)
async def waitForTitle(message: types.Message, state: FSMContext):
    title = message.text

    if len(title) > 40:
        await message.answer("Sorry, no more that 40 charasters in title")
    else:
        async with state.proxy() as data:
            data["title"] = title

            await PostStates.waitForContent.set()
            await message.answer("Okay, send me content for you post [ not necessary ]",
                                 reply_markup=dynamic_key.this(buttons[0]))


@dp.message_handler(content_types=types.ContentType.TEXT, state=PostStates.waitForContent)
async def waitForContent(message: types.Message, state: FSMContext):
    content = message.text
    
    if len(content) > 400:
        await message.answer("Sorry, no more that 400 charasters in content")
    else:
        async with state.proxy() as data:
            if content == buttons[0][0]:
                data["content"] = None
            else:
                data["content"] = content

            await PostStates.waitForOldMark.set()
            await message.answer("Okay, mark you post by age [ necessary ]",
                                 reply_markup=dynamic_key.this(buttons[1]))

@dp.message_handler(content_types=[types.ContentType.TEXT], state=PostStates.waitForOldMark)
async def waitForOldMark(message: types.Message, state: FSMContext):
    oldMark = message.text

    async with state.proxy() as data:
        if oldMark == buttons[1][0]:   data["oldMark"] = True
        elif oldMark == buttons[1][1]: data["oldMark"] = False
        else: await message.answer("Sorry, but it text not is from buttons")

        await PostStates.waitForTag.set()
        await message.answer("send me a word that is associated with the post (tag)",
                             reply_markup=dynamic_key.this(buttons[2]))


@dp.message_handler(content_types=types.ContentType.TEXT, state=PostStates.waitForTag)
async def waitForTag(message: types.Message, state: FSMContext):
    tag = message.text

    async with state.proxy() as data:
        if len(message.text) > 40:
            await message.answer("Sorry, no more that 40 characters")
        else:
            data["tag"] = tag if tag != buttons[2][0] else None

            await PostStates.waitForFinal.set()
            await message.answer("Okay, confrime your post",
                                reply_markup=dynamic_key.this(buttons[3]))


@dp.message_handler(content_types=types.ContentType.TEXT, state=PostStates.waitForFinal)
async def waitForFimal(message: types.Message, state: FSMContext):
    solution = message.text

    async with state.proxy() as data:
        if solution == buttons[3][0]:
            await db.post(
                id      = data["id"],
                title   = data["title"],
                content = data["content"],
                oldMark = data["oldMark"],
                tag     = data["tag"]
            )

            await state.finish()
            await message.answer("Your post is created")

        elif solution == buttons[3][1]:
            print(data)
            
            await message.answer("Decline your post.")
            await state.finish()

        else: await message.answer("there is no such solution")
