from aiogram import types
from aiogram.dispatcher import FSMContext
import asyncpg
from aiogram.dispatcher.filters.builtin import Command

from loader import dp, db
from data.config import ADMINS
from states.userStates import AddVideo
from keyboards.default.B12UserKeyboard import confirm


@dp.message_handler(Command(["add_video"]), state="*")
async def add_video(message: types):
    if message.from_user.id in ADMINS[0]:
        await message.answer("Video jo'nating")
        await AddVideo.start.set()
    else:
        await message.answer("You don't qualify bro :(")


@dp.message_handler(content_types=types.ContentTypes.VIDEO, state=AddVideo.start)
async def add_video(message: types, state: FSMContext):
    file_id = message.document.file_id
    await state.update_data({"file_id": file_id})
    await message.answer("Endi keyword jo'nating")
    await AddVideo.end.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=AddVideo.start)
async def add_video(message: types):
    await message.answer("Send me a video, you bastard")


@dp.message_handler(state=AddVideo.end, content_types=types.ContentTypes.TEXT)
async def add_text(message: types, state: FSMContext):
    keyword = message.text
    await state.update_data({"keyword": keyword})
    data_info = await state.get_data()
    file_id = data_info.get("file_id")
    await message.answer_document(document=file_id, thumb=file_id, caption=f"\nKalit so'z : <b>{keyword}</b>")
    await message.answer("Tasdiqlang:", reply_markup=confirm)
    await AddVideo.confirm.set()


@dp.message_handler(state=AddVideo.end, content_types=types.ContentTypes.ANY)
async def add_text(message: types):
    await message.answer("Send me text, you freaking bastard!")


@dp.message_handler(state=AddVideo.confirm, text="Confirm! ✅")
async def add_text(message: types, state: FSMContext):
    data = await state.get_data()
    try:
        db.add_video(
            keyword=data.get("keyword"),
            file_id=data.get("file_id")
        )
    except Exception as e:
        await message.reply_text(f"Couldn't add to database for {e} reason :(")
    await message.answer("Added successfully! 🙂")
    await state.finish()


@dp.message_handler(state=AddVideo.confirm, text="Edit ✏️")
async def add_text(message: types):
    await message.answer("Video jo'nating")
    await AddVideo.start.set()


@dp.message_handler(state=AddVideo.confirm, content_types=types.ContentTypes.ANY)
async def add_text(message: types):
    await message.answer("CLICK THE BUTTONS BRUUUH")


