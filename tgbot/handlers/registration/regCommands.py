from tgbot              import keyboards
from tgbot.states       import RegStates
from loader             import dp

from aiogram            import types
from aiogram.dispatcher import FSMContext

buttons = [
    ['Rejection of the description'], 
    ['Ukrainian 🇺🇦', 'Polish 🇵🇱', 'English 🇬🇧'], 
    ['Accept', 'Reject']
]

@dp.message_handler(commands=["reg"])
async def reg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["uid"] = message.from_user.id
    
    await RegStates.waitForName.set()
    await message.answer(
        "great, let's start our registration process! Enter your name(no more than 30 letters)"
    )


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=RegStates.waitForName)
async def waitForName(message: types.Message, state: FSMContext):
    name = message.text.capitalize()

    if len(name) > 30:
        await message.anwser("Sorry, but your name is more than 30 letters")
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
        await message.answer("Sorry, but your age is not numeric number")
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
        await message.answer("Okay, next.")
    else:
        if len(description) > 300:
            await message.answer("Sorry, no more than 300 letters")
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
    else: message.answer("sorry, this language not exists")

    async with state.proxy() as data:
        data["language"] = choice
    
    await RegStates.waitForConfrime.set()
    await message.answer(
        "great, confrime!",
        reply_markup=keyboards.replyKeyboard(buttons[2])
    )

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=RegStates.waitForConfrime)
async def waitForConfrime(message: types.Message, state: FSMContext):
    choice = message.text
    
    if choice == buttons[2][0]:
        async with state.proxy() as data:
            await message.answer(data)
        
        await state.finish()
    elif choice == buttons[2][1]:
        await message.answer("cancel")
        await state.finish()
    else: await message.answer("not exists")
