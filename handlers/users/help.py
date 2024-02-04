from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp(), state="*")
async def bot_help(message: types.Message):
    text = ("Commands: ",
            "/start - Qaytadan boshlash",
            "/add - Formani to'ldirish",
            "/results - Natijalarni ko'rish",
            "/help - Yordam olish")
    
    await message.answer("\n".join(text))