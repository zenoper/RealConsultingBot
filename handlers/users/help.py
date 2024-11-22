from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from data.config import ADMINS


@dp.message_handler(CommandHelp(), state="*")
async def bot_help(message: types.Message):
    if str(message.from_user.id) not in ADMINS:
        text = ("Commands: ",
                "/start - Qaytadan boshlash",
                "/add - Formani to'ldirish",
                "/results - Natijalarni ko'rish",
                "/help - Yordam olish")

        await message.answer("\n".join(text))
    else:
        text = ("Commands: ",
                "/start - Qaytadan boshlash",
                "/download_data - Export all data bro",
                "/add - Formani to'ldirish",
                "/results - Natijalarni ko'rish",
                "/help - Yordam olish")

        await message.answer("\n".join(text))