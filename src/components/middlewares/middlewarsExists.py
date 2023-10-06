from loader                         import dp, db
from aiogram                        import types
from aiogram.dispatcher             import FSMContext
from aiogram.dispatcher.middlewares import BaseMiddleware


class MidExists(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data):
        if message.text.startswith(("/start", "/help", "/reg", "/deactivation")):
            return True
        else:
            try:
                if await db.hook_exists(message.from_user.id):
                    return True
                else:
                    await message.answer("Please, register via /reg")
                    return False
            except Exception as e:
                print(f"Database error: {str(e)}")
                return False
        return True