from aiogram.dispatcher             import FSMContext
from loader                         import dp, db
from aiogram                        import types

from src.components.states          import RegStates
from src.components.keyboards.reply import dynamic_key

buttons = [
    ["[ Give my telegram nickname. ]"],
    ["[ I don't want to give my age. ]"],
    ["[ I don't want to give my city ]"],
    [
        "[ Confrime [ 🚀 ] ]",
        "[ Decline  [ 🛑 ] ]"
    ]
]

@dp.message_handler(commands=["deactivation"])
async def deactivation(message: types.Message):
    await RegStates.waitForDeleting.set()
    await message.answer("good, confrime deleting your account",
                         reply_markup=dynamic_key.this(buttons[3]))

@dp.message_handler(commands=["reg"])
async def reg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["id"] = message.from_user.id

    await RegStates.waitForNickname.set()
    await message.answer(text="In this case. register! Send you're name.", reply_markup=dynamic_key.this(buttons[0]))


@dp.message_handler(content_types=[types.ContentType.TEXT], state=RegStates.waitForNickname)
async def nickname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text != buttons[0][0]:
            data["nickname"] = message.text
        else:
            data["nickname"] = message.from_user.full_name
        
    await RegStates.waitForAge.set()
    await message.answer(text="Okay, give me you're age", reply_markup=dynamic_key.this(buttons[1]))


@dp.message_handler(content_types=[types.ContentType.TEXT], state=RegStates.waitForAge)
async def age(message: types.Message, state: FSMContext):
    content: str = message.text

    async with state.proxy() as data:
        if content != buttons[1][0]:
            if content.isdigit():
                if int(content) > 8:
                    data["age"] = int(content)
                    await RegStates.waitForCity.set()
                    await message.answer(text="Give me you're sity-name", 
                                         reply_markup=dynamic_key.this(buttons[2]))
                else:
                    await message.answer("Enter your realy age")
            else:
                await message.answer("Sorry, but your anwser must be integer.")
        else:
            data["age"] = 0
            
            await RegStates.waitForCity.set()
            await message.answer(text="Give me you're sity-name", 
                                 reply_markup=dynamic_key.this(buttons[2]))


@dp.message_handler(content_types=[types.ContentType.TEXT], state=RegStates.waitForCity)
async def city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text != buttons[2][0]:
            data["city"] = message.text
        
            await RegStates.waitForConf.set()
            await message.answer("Okay. Confrime you're registration", 
                                 reply_markup=dynamic_key.this(buttons[3]))
        else:
            data["city"] = "unknown"
            await RegStates.waitForConf.set()
            await message.answer("Okay. Confrime you're registration", 
                                 reply_markup=dynamic_key.this(buttons[3]))


@dp.message_handler(text=buttons[3][0], state=[RegStates.waitForConf, RegStates.waitForDeleting])
async def confrime(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    

    print(current_state)
    if current_state == "RegStates:waitForConf":
        async with state.proxy() as data:
            await db.reg(
                data["id"],
                data["nickname"],
                data["age"],
                data["city"]
            )

            await state.finish()
            await message.answer("You're finish registration!🌟")
    
    elif current_state == "RegStates:waitForDeleting":
        await message.answer("Okay, i will delete your account and your posts")
        await message.answer(text=(await db.deactivation(message.from_user.id)))
        await state.finish()

@dp.message_handler(text=buttons[3][1], state=[RegStates.waitForConf, RegStates.waitForDeleting])
async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    

    if current_state == "RegStates:waitForConf":
        await state.finish()
        await message.answer("Okay, cancel your registration form")
    elif current_state == "RegStates:waitForDeleting":
        await message.answer("Okay, i cancel deleting a account")
        await state.finish()