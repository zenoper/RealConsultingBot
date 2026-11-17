from aiogram import F, types
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums import ContentType

from loader import dp, db, bot
from states.userStates import UserState, ResultState
from keyboards.default import UserKeyboard
from data.config import ADMINS


@dp.message(F.content_type == ContentType.TEXT, CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        await message.answer(f"Assalamu alaykum, boshliq! 🙂\n\nYour commands: \n/download_data -> export all F1 data",
                             reply_markup=UserKeyboard.start)
        await state.set_state(UserState.start)
    else:
        await message.answer(f"Assalamu alaykum, <b>{message.from_user.full_name}</b>! 🙂\n\nTanlang: \n\nChoose:", reply_markup=UserKeyboard.start)
        await state.set_state(UserState.start)


@dp.message(StateFilter(ResultState.results), F.text == "Anketa to'ldirish")
@dp.message(StateFilter(UserState.start), F.text == "Anketa to'ldirish")
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer(f"Iltimos, to'liq ism va familiyangizni kiriting! \n\nPlease, fill in your full name!")
    await state.set_state(UserState.fullname)


async def send_video_by_index(chat_id, index):
    # Create inline keyboard
    data = await db.select_all_videos()
    if data:
        buttons = []
        if index > 0:
            buttons.append(types.InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"video_{index - 1}"))
        if index < len(data) - 1:
            buttons.append(types.InlineKeyboardButton(text="Oldinga ➡️", callback_data=f"video_{index + 1}"))

        markup = types.InlineKeyboardMarkup(inline_keyboard=[buttons]) if buttons else None

        # Send the video
        await bot.send_video(chat_id, video=data[index][3], caption=data[index][2], reply_markup=markup)
    else:
        await bot.send_message(text="No videos found, /add_video", chat_id=chat_id)


@dp.message(StateFilter(UserState.start), F.text == "Natijalarni ko'rish")
async def watch_video(message: types.Message, state: FSMContext):
    await send_video_by_index(message.chat.id, 0)
    await state.set_state(ResultState.results)


@dp.callback_query(StateFilter(ResultState.results), lambda c: c.data and c.data.startswith('video_'))
async def handle_video_navigation(callback_query: types.CallbackQuery):
    # Extract the video index from the callback data/
    index = int(callback_query.data.split('_')[1])

    # Edit the message with the new video
    await callback_query.message.delete()
    await send_video_by_index(callback_query.message.chat.id, index)

