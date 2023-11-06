from tgbot              import keyboards, utils
from loader             import dp, db

from aiogram            import types

messageTexts = {
    "find": "find - це окремий модуль пошуків, в який входять такі команди як:\nfindpr, findps та їх id версії(findprId, findpsId), де перша команда - шукає профілі, друга - пости, а їх id версії - це пошук по id",
    "aid" : "Answer ID - це ID поста на якого відповідають у пості, наприклад\nпост має ID x, відповідає на запиз з ID y, для поста з ID х - ID y є АID"
}

@dp.message_handler(commands=["help"])
async def help(message: types.Message):
    try:
        async with db as slot:
            user = (await slot.isExists(message.from_user.id))[0]
            if user:
                userLang = user["language"]
                msg = message.text.lower().split()
                if len(msg) == 1:
                    await utils.transWarn(
                        message, "Будь ласка, це версія команди help без аргументів\nДоповніть до /help одне з ключевих слів\n find", userLang, timer=7
                    )
                else:
                    if msg[-1] in messageTexts.keys():
                        await utils.translateText(
                            message, messageTexts[-1], userLang
                        )
                    
                    else:
                        await utils.transWarn(
                            message, f"Вибачте, але такої опції  не існує, існує тільки модуль", userLang, timer=7
                        )
                        await utils.warn(message, " ".join(messageTexts.keys()))
    except Exception as e:
        print(e)
        await utils.warn(message, "Sorry, something wrong, maybe you not register. \n/reg")