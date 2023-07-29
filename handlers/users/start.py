from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from states.userStates import UserState


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Assalamu alaykum, {message.from_user.full_name}!\n Iltimos, to'liq ismingizni kiriting!")
    await UserState.fullname.set()
