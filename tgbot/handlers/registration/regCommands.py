from tgbot              import keyboards, utils
from tgbot.states       import RegStates
from loader             import dp, db

from aiogram            import types
from aiogram.dispatcher import FSMContext

buttons = [
    ['Rejection of the description'], 
    ['Ukrainian 🇺🇦', 'Polish 🇵🇱', 'English 🇬🇧'], 
    ['Confirm', 'Contradict'],
    ['Yes', 'No']
]


@dp.message_handler(commands=["reg"])
async def reg(message: types.Message, state: FSMContext):
    uid = message.from_user.id
    
    async with state.proxy() as data:
        async with db as slot:
            data["exist?"] = True if (await slot.isExists(uid)) else False
            data["uid"]    = uid

            print(data["exist?"])

    await RegStates.waitForLanguage.set()
    await message.answer(text="great, let's start our registration process! Enter your language", 
                         reply_markup=keyboards.replyKeyboard(buttons[1]))
    
@dp.message_handler(content_types=types.ContentTypes.TEXT, state=RegStates.waitForLanguage)
async def waitForLanguage(message: types.Message, state: FSMContext):
    language = message.text
    choice = None

    if language == buttons[1][0]: choice = "uk"
    elif language == buttons[1][1]: choice = "pl"
    elif language == buttons[1][2]: choice = "en"
    
    async with state.proxy() as data:
        if choice in ["uk", "pl", "en"]:
            data["language"] = choice
            
            await RegStates.waitForName.set()
            await utils.translateText(
                message,
                "great, confirm! Enter your name.",
                data["language"]
            )
        else: await utils.transWarn(message, "sorry, this language not exists", data["language"])

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=RegStates.waitForName)
async def waitForName(message: types.Message, state: FSMContext):
    name = message.text.capitalize()

    async with state.proxy() as data:
    
        if len(name) > 30:
            await utils.transWarn( message, "good, let's enter your age!", data["language"])
        else:
            data["name"] = name
            await RegStates.waitForAge.set()
            await utils.translateText(message, "good, let's enter your age!", data["language"])

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=RegStates.waitForAge)
async def waitForAge(message: types.Message, state: FSMContext):
    age = message.text

    async with state.proxy() as data:
        if not age.isdigit():
            await utils.transWarn(message, "Sorry, but your age is not numeric number")
        else:
            data["age"] = int(age)
            
            await RegStates.waitForDescription.set()
            await utils.translateText(
                message,
                "Well well well, enter your description(your hobbies, intereses)",
                data["language"],
                markup=keyboards.reply.replyKeyboard(buttons[0])
            )


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=RegStates.waitForDescription)
async def waitForDescription(message: types.Message, state: FSMContext):
    description = message.text
    localState = None

    
    async with state.proxy() as data:
        if description == buttons[0][0]:

            data["description"] = localState
            await RegStates.waitForProfile.set()
            
            await utils.transWarn(message, "Okay, next.", data['language'], timer=2)
            await utils.translateText(
                message,
                "great, choice permission for your profile(if you decline then we will don't place link on you!)\n\n\n\nDo you want us to show your username with a link when displaying your profile?",
                data["language"],
                markup=keyboards.replyKeyboard(buttons[-1])
            )
        else:
            try:
                if len(description) > 300:
                    raise ValueError('longer')
                else:
                    localState = description

                data["description"] = localState
            
                await RegStates.waitForProfile.set()
                await utils.translateText(
                    message,
                    "great, choice permission for your profile(if you decline then we will don't place link on you!)\n\n\n\nDo you want us to show your username with a link when displaying your profile?",
                    data["language"],
                    markup=keyboards.replyKeyboard(buttons[-1])
                )
            except ValueError:
                await utils.transWarn(message, "Sorry, no more than 300 letters", data['language'])


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=RegStates.waitForProfile)
async def waitForProfile(message: types.Message, state: FSMContext):
    choice = message.text
    choose = None

    async with state.proxy() as data:
        try:
            if choice == buttons[-1][0]:    choose = True
            elif choice == buttons[-1][1]:  choose = False
            else: raise ValueError('not exist')
            
            print(choose)
            data['profile'] = choose

            await RegStates.waitForConfirm.set()
            await utils.translateText(
                message,
                "great, confirm!",
                data["language"],
                markup=keyboards.replyKeyboard(buttons[2])
            )

        except ValueError:
            await utils.transWarn(message, "sorry, this language not exists", data['language'])

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=RegStates.waitForConfirm)
async def waitForConfirm(message: types.Message, state: FSMContext):
    choice = message.text
    
    async with state.proxy() as data:
        if choice == buttons[2][0]:
            async with db as slot: 
                await slot.userCreate(
                    tid         = data["uid"],
                    name        = data["name"],
                    age         = data["age"],
                    description = data["description"],
                    language    = data["language"],
                    profile     = data["profile"],
                    exist       = data["exist?"]
                )

            await utils.translateText(message, "Ви пройшли регістрацію!", data["language"])
            await state.finish()
        elif choice == buttons[2][1]:
            await utils.translateText(message, "cancel", data["language"])
            await state.finish()
        else: await utils.transWarn(message, "not exists", data["language"])


@dp.message_handler(commands=["deactivation"])
async def deactivation(message: types.Message):
    uid = message.from_user.id
    async with db as slot: 
        if (await slot.isExists(uid)):
            await slot.userDelete(uid)
        else:
            await utils.warn(message, "you're not exist")