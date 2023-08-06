from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from states.userStates import UserState


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Assalamu alaykum, <b>{message.from_user.full_name}</b>! 🙂\n \nIltimos, to'liq ism va familiyangizni kiriting! \n\nPlease, fill in your full name!")
    await UserState.fullname.set()
