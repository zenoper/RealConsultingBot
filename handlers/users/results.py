from aiogram import types

from loader import dp
from aiogram.dispatcher.filters.builtin import Command

from .start import send_video_by_index
from states.userStates import ResultState, UserState
from keyboards.default import UserKeyboard


@dp.message_handler(Command(["results"]), state="*")
async def results(message: types):
    await send_video_by_index(message.chat.id, 0)
    await ResultState.results.set()


@dp.message_handler(state=ResultState.results, content_types=types.ContentTypes.ANY)
async def results(message: types):
    await message.answer(f"Assalamu alaykum, <b>{message.from_user.full_name}</b>! 🙂\n\nTanlang: \n\nChoose:",
                         reply_markup=UserKeyboard.start)
    await UserState.start.set()