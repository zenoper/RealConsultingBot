from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp
from states.userStates import B1orF1States, B1UserState
from keyboards.default import UserKeyboard, B12UserKeyboard
from states.userStates import UserState


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Assalamu alaykum, <b>{message.from_user.full_name}</b>! 🙂\n \nIltimos, to'liq ism va familiyangizni kiriting! \n\nPlease, fill in your full name!")
    await UserState.fullname.set()


@dp.message_handler(state=UserState.fullname)
async def fullname(message: types.Message, state: FSMContext):
    full_name = message.text
    if len(full_name) <= 5:
        await message.answer(
            "Iltimos, ism va familiyangizni <b>to'liq</b> kiriting! \n\nPlease, fill in your name and surname <b>completely</b>!")
    else:
        await state.update_data({"fullname": full_name})
        await state.update_data({"qualification": 0})
        await message.answer("Iltimos, tug'ilgan kun, oy, va yilingizni kiriting! \n\nPlease, fill in your birthdate!")
        await UserState.date_of_birth.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=UserState.fullname)
async def fullname(message: types.Message):
    await message.answer("Iltimos, faqatgina harflardan foydalaning! \n\nPlease, only use letters!")


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=UserState.date_of_birth)
async def birthdate(message: types.Message, state: FSMContext):
    date_of_birth = message.text
    username = message.from_user.username
    telegram_id = message.from_user.id
    if username:
        if len(date_of_birth) <= 5:
            await message.answer(
                "Iltimos, tug'ilgan kun, oy, va yilingizni <b>to'liq</b> kiriting! \n\nPlease, fill in your <b>complete</b> birthdate!")
        else:
            await state.update_data({"date_of_birth": date_of_birth, "username": username, "telegram_id": telegram_id})
            await message.answer("Qaysi turdagi visani olmoqchisiz? \n\nWhat is the type of visa you want to take?",
                                 reply_markup=UserKeyboard.b1orf1)
            await B1orF1States.start.set()
    else:
        await message.answer(
            "Iltimos, telegram profilingizga username qo'shing. \nShunda sizga aloqaga chiqa olamiz. \n\nPlease, add a username to your telegram profile. Then, we can contact you!")


@dp.message_handler(content_types=types.ContentTypes.ANY, state=UserState.date_of_birth)
async def dateofbirth(message: types.Message):
    await message.answer("Iltimos, faqatgina harflardan foydalaning! \n\nPlease, only use letters!")


@dp.message_handler(state=B1orF1States.start, text="F1")
async def start(message: types.Message):
    await message.answer("O'zbekistonda istiqomat qilasizmi yoki chet-eldami? \n\nDo you live in Uzbekistan or abroad?",
                         reply_markup=UserKeyboard.intorlocal)
    await UserState.interORlocal.set()


@dp.message_handler(state=B1orF1States.start, text="B1/B2")
async def start(message: types.Message):
    await message.answer("Chet-elda oldin bo'lgansiz? \n\nHave you been aboard?",
                         reply_markup=B12UserKeyboard.countries)
    await B1UserState.abroad.set()


@dp.message_handler(state=B1orF1States, content_types=types.ContentTypes.ANY)
async def start(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing!", reply_markup=UserKeyboard.b1orf1)
