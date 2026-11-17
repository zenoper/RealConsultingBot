from aiogram import F, types
from aiogram.filters import StateFilter
from aiogram.enums import ContentType

from loader import dp


# Echo bot
@dp.message(StateFilter(None), F.content_type == ContentType.TEXT)
async def bot_echo(message: types.Message):
    await message.answer(message.text)
