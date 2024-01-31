import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from states.userStates import B1UserState
from keyboards.default import B12UserKeyboard
from aiogram.types import ReplyKeyboardRemove
from data.config import ADMINS


@dp.message_handler(state=B1UserState.abroad, text="Yes/Ha")
async def abroad(message: types):
    await message.answer("Iltimos, siz bo'lgan davlatlar nomi yozib qoldiring")
    await B1UserState.countries.set()


@dp.message_handler(state=B1UserState.abroad, text="No/Yo'q")
async def abroad(message: types):
    await message.answer("Iltimos, siz bo'lgan davlatlar nomi yozib qoldiring")
    await B1UserState.countries.set()


@dp.message_handler(state=B1UserState.abroad, content_types=types.ContentTypes.ANY)
async def abroad(message: types):
    await message.answer("Iltimos, tugmalardan birini bosing! \n\nPlease, click one of the buttons",
                         reply_markup=B12UserKeyboard.countries)
    await B1UserState.countries.set()