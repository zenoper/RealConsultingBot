from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ContentType

from loader import dp
from states.userStates import UserState
from aiogram.types import ReplyKeyboardRemove


@dp.message(F.content_type == ContentType.TEXT, Command('add'))
async def results(message: types, state: FSMContext):
    await message.answer(f"Iltimos, to'liq ism va familiyangizni kiriting! \n\nPlease, fill in your full name!", reply_markup=ReplyKeyboardRemove(selective=False))
    await state.set_state(UserState.fullname)