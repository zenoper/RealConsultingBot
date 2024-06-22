from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram import types

from loader import dp, db, bot
from states.userStates import UserState, ResultState
from keyboards.default import UserKeyboard


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message):
    await message.answer(f"Assalamu alaykum, <b>{message.from_user.full_name}</b>! 🙂\n\nTanlang: \n\nChoose:", reply_markup=UserKeyboard.start)
    await UserState.start.set()


@dp.message_handler(state=ResultState.results, text="Anketa to'ldirish")
@dp.message_handler(state=UserState.start, text="Anketa to'ldirish")
async def bot_start(message: types.Message):
    await message.answer(f"Iltimos, to'liq ism va familiyangizni kiriting! \n\nPlease, fill in your full name!")
    await UserState.fullname.set()


async def send_video_by_index(chat_id, index):
    # Create inline keyboard
    data = await db.select_all_videos()
    if data:
        markup = types.InlineKeyboardMarkup(row_width=2)
        buttons = []
        if index > 0:
            buttons.append(types.InlineKeyboardButton("⬅️ Orqaga", callback_data=f"video_{index - 1}"))
        if index < len(data) - 1:
            buttons.append(types.InlineKeyboardButton("Oldinga ➡️", callback_data=f"video_{index + 1}"))

        markup.add(*buttons)

        # Send the video
        await bot.send_video(chat_id, video=data[index][3], caption=data[index][2], reply_markup=markup)
    else:
        await bot.send_message(text="No videos found, /add_video", chat_id=chat_id)


@dp.message_handler(state=UserState.start, text="Natijalarni ko'rish")
async def watch_video(message: types.Message):
    await send_video_by_index(message.chat.id, 0)
    await ResultState.results.set()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('video_'), state=ResultState.results)
async def handle_video_navigation(callback_query: types.CallbackQuery):
    # Extract the video index from the callback data/
    index = int(callback_query.data.split('_')[1])

    # Edit the message with the new video
    await callback_query.message.delete()
    await send_video_by_index(callback_query.message.chat.id, index)

