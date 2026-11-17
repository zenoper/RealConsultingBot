from aiogram import F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums import ContentType

from loader import dp

from .start import send_video_by_index
from states.userStates import ResultState, UserState
from keyboards.default import UserKeyboard


@dp.message(F.content_type == ContentType.TEXT, Command('results'))
async def results(message: types, state: FSMContext):
    await send_video_by_index(message.chat.id, 0)
    await state.set_state(ResultState.results)


@dp.message(StateFilter(ResultState.results))
async def results(message: types, state: FSMContext):
    await message.answer(f"Assalamu alaykum, <b>{message.from_user.full_name}</b>! 🙂\n\nTanlang: \n\nChoose:",
                         reply_markup=UserKeyboard.start)
    await state.set_state(UserState.start)