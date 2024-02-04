from aiogram import types
from aiogram.dispatcher import FSMContext
import asyncpg
import aiogram
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from loader import dp, db
from data.config import ADMINS
from states.userStates import AddVideo, DeleteStates, UserState
from keyboards.default.B12UserKeyboard import confirm


@dp.message_handler(Command(["add_video"]), state="*")
async def add_video(message: types):
    if str(message.from_user.id) == ADMINS[0]:
        await message.answer("Video jo'nating")
        await AddVideo.start.set()
    else:
        await message.answer("You don't qualify bro :(")


@dp.message_handler(content_types=types.ContentTypes.VIDEO, state=AddVideo.start)
async def add_video(message: types, state: FSMContext):
    file_id = message.video.file_id
    await state.update_data({"file_id": file_id})
    await message.answer("Endi keyword jo'nating")
    await AddVideo.end.set()


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT, state=AddVideo.start)
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
    await message.answer("Now, send me the caption")
    await AddVideo.caption.set()


@dp.message_handler(state=AddVideo.end, content_types=types.ContentTypes.ANY)
async def add_text(message: types):
    await message.answer("Send me text, you freaking bastard!")


@dp.message_handler(state=AddVideo.caption, content_types=types.ContentTypes.TEXT)
async def add_text(message: types, state: FSMContext):
    try:
        caption = message.text
        await state.update_data({"caption": caption})
        data_info = await state.get_data()
        file_id = data_info.get("file_id")
        keyword = data_info.get("keyword")
        await message.answer_document(document=file_id, thumb=file_id, caption=f"{caption} \n\nKalit so'z : <b>{keyword}</b>")
        await message.answer("Tasdiqlang:", reply_markup=confirm)
        await AddVideo.confirm.set()
    except aiogram.utils.exceptions.BadRequest:
        await message.answer("Caption or Keyword is too long!")


@dp.message_handler(state=AddVideo.caption, content_types=types.ContentTypes.ANY)
async def add_text(message: types):
    await message.answer("Only text bro!")


@dp.message_handler(state=AddVideo.confirm, text="Confirm! ✅")
async def add_text(message: types, state: FSMContext):
    data = await state.get_data()
    try:
        await db.add_video(
            keyword=data.get("keyword"),
            caption=data.get("caption"),
            file_id=data.get("file_id")
        )
        await message.answer("Added successfully! 🙂")
    except Exception as e:
        await message.answer(f"Couldn't add to database because:  <b>{e}</b> ")
    await state.finish()


@dp.message_handler(state=AddVideo.confirm, text="Edit ✏️")
async def add_text(message: types):
    await message.answer("Video jo'nating")
    await AddVideo.start.set()


@dp.message_handler(state=AddVideo.confirm, content_types=types.ContentTypes.ANY)
async def add_text(message: types):
    await message.answer("CLICK THE BUTTONS BRUUUH")


# DELETE VIDEO

@dp.message_handler(Command(["delete_video"]), state="*")
async def add_video(message: types):
    if str(message.from_user.id) == ADMINS[0]:
        await DeleteStates.select.set()
        videos = await db.select_all_videos()
        if videos:
            delete_video = InlineKeyboardMarkup(
                inline_keyboard=[

                ]
            )
            for video in videos:
                delete_video.inline_keyboard.append([
                    InlineKeyboardButton(text=video[1], callback_data=video[1])
                ], )
            await message.answer("Qaysi ma'lumotni o'chirishni istaysiz?", reply_markup=delete_video)
        else:
            await message.answer(
                "Sizda hozircha hech qanday ma'lumotlar saqlamagansiz. \n\nMa'lumot qo'shish uchun /add_video buyrug'ini bering")
            await UserState.start.set()
    else:
        await message.answer("You don't qualify bro :(")
        await UserState.start.set()


@dp.callback_query_handler(state=DeleteStates.select)
async def delete(call: CallbackQuery):
    callback_data = call.data
    video = await db.select_video(keyword=str(callback_data))
    if video:
        delete_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="o'chirish", callback_data=video[1])
                ],
            ]
        )
        try:
            await call.message.answer_video(video=video[3], thumb=video[3], caption=video[2],
                                            reply_markup=delete_keyboard)
            await DeleteStates.delete.set()
        except Exception as e:
            await call.message.answer(f"Couldn't delete video bro. Here is the '{e}' mistake. Probably coz of keyword unique contraint has been broken.")

    else:
        await call.answer("Iltimos, tugmalardan birini tanlang!")


@dp.callback_query_handler(state=DeleteStates.delete)
async def delete(call: CallbackQuery):
    try:
        await db.delete_video(keyword=call.data)
        await call.message.answer("O'chirish muvaffaqiyatli amalga oshdi!")
        await UserState.start.set()
    except Exception as e:
        await call.message.answer("O'chirish amalga oshmadi. Uzr :( \n\nQaytadan harakat qilib ko'ring : /delete")
        print(e)