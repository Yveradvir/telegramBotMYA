from tgbot              import keyboards, utils
from tgbot.states       import RegStates
from loader             import dp, db

from aiogram            import types
from aiogram.dispatcher import FSMContext

buttons = [
    ['Rejection of the description'], 
    ['Ukrainian 🇺🇦', 'Polish 🇵🇱', 'English 🇬🇧'], 
    ['Accept', 'Reject']
]

@dp.message_handler(commands=["test"])
async def second_step(message: types.Message):
    my_test = (await db.select_test_info())
    print(my_test)

@dp.message_handler(commands=["reg"])
async def reg(message: types.Message, state: FSMContext):
    uid = message.from_user.id
    async with state.proxy() as data:
        data["uid"] = uid
    
    await RegStates.waitForName.set()
    await message.answer(
        "great, let's start our registration process! Enter your name(no more than 30 letters)"
    )


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=RegStates.waitForName)
async def waitForName(message: types.Message, state: FSMContext):
    name = message.text.capitalize()

    if len(name) > 30:
        await utils.warn(message, "Sorry, but your name is more than 30 letters")
    else:
        async with state.proxy() as data:
            data["name"] = name
        
        await RegStates.waitForAge.set()
        await message.answer(
            "goof, let's enter your age!"
        )

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=RegStates.waitForAge)
async def waitForAge(message: types.Message, state: FSMContext):
    age = message.text

    if not age.isdigit():
        await utils.warn(message, "Sorry, but your age is not numeric number")
    else:
        async with state.proxy() as data:
            data["age"] = age
        
        await RegStates.waitForDescription.set()
        await message.answer(
            "Well well well, enter your description(your hobbies, intereses)",
            reply_markup=keyboards.reply.replyKeyboard(buttons[0])
        )


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=RegStates.waitForDescription)
async def waitForDescription(message: types.Message, state: FSMContext):
    description = message.text
    localState = None

    if description == buttons[0]:
        await utils.warn(message, "Okay, next.")
    else:
        if len(description) > 300:
            await utils.warn(message, "Sorry, no more than 300 letters")
            localState = "Please, please re-register, so your description is longer than 300 characters"
        else:
            localState = description

    async with state.proxy() as data:
        data["description"] = localState
    
    await RegStates.waitForLanguage.set()
    await message.answer(
        "great, choice your language!",
        reply_markup=keyboards.replyKeyboard(buttons[1])
    )

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=RegStates.waitForLanguage)
async def waitForLanguage(message: types.Message, state: FSMContext):
    language = message.text
    choice = None

    if language == buttons[1][0]: choice = "ua"
    elif language == buttons[1][1]: choice = "pl"
    elif language == buttons[1][2]: choice = "en"
    
    if choice in ["ua", "pl", "en"]:
        async with state.proxy() as data:
            data["language"] = choice
        
        await RegStates.waitForConfrime.set()
        await message.answer(
            "great, confrime!",
            reply_markup=keyboards.replyKeyboard(buttons[2])
        )
    else: await utils.warn(message, "sorry, this language not exists")

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=RegStates.waitForConfrime)
async def waitForConfrime(message: types.Message, state: FSMContext):
    choice = message.text
    
    if choice == buttons[2][0]:
        async with state.proxy() as data:
            async with db as slot: 
                await slot.userCreate(
                    tid         = data["uid"],
                    name        = data["name"],
                    age         = data["age"],
                    description = data["description"],
                    language    = data["language"]
                )

        await state.finish()
    elif choice == buttons[2][1]:
        await message.answer("cancel")
        await state.finish()
    else: await message.answer("not exists")


@dp.message_handler(commands=["deactivation"])
async def deactivation(message: types.Message):
    uid = message.from_user.id
    async with db as slot: 
        a = (await slot.isExists(uid))
        print(a)
    await message.answer("Okay, confrime it")