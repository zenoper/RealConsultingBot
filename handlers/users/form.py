from aiogram import types

from loader import dp
from aiogram.dispatcher.filters.builtin import Command
from states.userStates import UserState
from aiogram.types import ReplyKeyboardRemove


@dp.message_handler(Command(["add"]), state="*")
async def results(message: types):
    await message.answer(f"Iltimos, to'liq ism va familiyangizni kiriting! \n\nPlease, fill in your full name!", reply_markup=ReplyKeyboardRemove(selective=False))
    await UserState.fullname.set()