from tgbot              import keyboards, utils
from tgbot.states       import PostStates
from loader             import dp, db

from aiogram            import types
from aiogram.dispatcher import FSMContext

buttons = [
    ["Reject"],
    ["Confirm", "Contradict"]
]

@dp.message_handler(commands=["npost"])
async def npost(message: types.Message, state: FSMContext):
    
    async with state.proxy() as data:
        async with db as slot:
            aboutUser = (await slot.isExists(message.from_user.id))[0]
            data["lang"] = aboutUser["language"]
            data["uid"]  = aboutUser["id"]
            print(data["lang"])

        await PostStates.waitForTitle.set()
        await utils.messageUtils.translateText(
            message=message,
            text="Прекрасно, тепер надайте заголовок вашого поста",
            lang=data["lang"]
        )

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=PostStates.waitForTitle)
async def postWaitForTitle(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            print(data["lang"])
            if len(message.text) <= 50:
                data["title"] = message.text 
        
                await PostStates.waitForContent.set()
                await utils.messageUtils.translateText(
                    message,
                    "Прекрасно, тепер надайте заголовок вашого поста",
                    data["lang"]
                )
            else: raise ValueError("Not correct")
        except ValueError:
            await utils.messageUtils.translateText(
                message, "Вибачте, але ваш заголовок більше за 50 символів",
                data["lang"]
            ) 

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=PostStates.waitForContent)
async def postWaitForContent(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            if len(message.text) <= 500:
                data["content"] = message.text

                await PostStates.waitForAnwserId.set()
                await utils.messageUtils.translateText(
                    message,
                    "Надайте ID поста, на який ви хочете відповісти(ви можете відмовитись)",
                    data["lang"], markup=keyboards.replyKeyboard(buttons[0])
                )
            else:
                raise ValueError("Not correct")
        except ValueError:
            await utils.messageUtils.translateText(
                message, "Вибачте, але ваш опис більше за 500 символів", data["lang"]
            )

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=PostStates.waitForAnwserId)
async def postwaitForAnwserId(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_text = str(message.text)
        print(message_text)
        try:
            if message_text == "reject":
                print("This is true")
                data["aid"] = None  # Fix the assignment here
                await PostStates.waitForConfirm.set()
                await utils.messageUtils.translateText(
                    message,
                    "Добре, враховуйте, що ви не відповіли на пост, але на ваш - можуть.\nПідтвердіть, будь-ласка",
                    data["lang"], keyboards.replyKeyboard(buttons[1])
                )
            else:
                print("This is false")
                if message_text.isdigit():
                    async with db as slot:
                        if await slot.isExistsPost(message_text):  # Check if post exists
                            data["aid"] = message_text
                            await PostStates.waitForConfirm.set()
                            await utils.messageUtils.translateText(
                                message,
                                "Підтвердіть, будь-ласка",
                                data["lang"], keyboards.replyKeyboard(buttons[1])
                            )
                        else:
                            raise Exception("Post with this ID does not exist")
                else:
                    raise TypeError("Sorry, not a digit")
        except TypeError as e:
            await utils.messageUtils.translateText(
                message, "ID повідомленнь тільки цифрові",
                data["lang"]
            )
        except Exception as e:
            await utils.messageUtils.translateText(
                message, "Вибачте, але такого ID поста не існує",
                data["lang"]
            )
            print(e)

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=PostStates.waitForConfirm)
async def postWaitForConfirm(message: types.Message, state: FSMContext):
    choice = message.text

    if choice == buttons[2][0]:
        async with state.proxy() as data:
            async with db as slot: 
                await slot.postCreate(
                    title        = data["name"],
                    description  = data["content"],
                    answer_id    = data["aid"],
                    author_id    = data["uid"],

                )

        await state.finish()
    elif choice == buttons[2][1]:
        async with state.proxy() as data:
            await utils.messageUtils.translateText(message, "canceled", data["lang"])
        await state.finish()
    else:
        async with state.proxy() as data:
            await utils.messageUtils.translateText(message, "This answer is not exists", data["lang"]) 
        await message.answer("") 
