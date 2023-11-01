from tgbot              import keyboards, utils
from loader             import dp, db

from aiogram            import types

messageTexts = {
    "find": "find - це окремий модуль пошуків, в який входять такі команди як:\nfindpr, findps та їх id версії(findprId, findpsId), де перша команда - шукає профілі, друга - пости, а їх id версії - це пошук по id"
}

@dp.message_handler(commands=["help"])
async def help(message: types.Message):
    try:
        print(message.text)
        user = (await db.isExists(message.from_user.id))[0]
        if user:
            userLang = user["language"]
            
            await utils.messageUtils(
                message, "Будь ласка, це версія команди help без аргументів\nДоповніть до /help одне з ключевих слів\n find"
            )
            
    except Exception as e:
        print(e)
        await message.answer("sorry, something wrong...")