from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from states.userStates import UserState

from keyboards.default import UserKeyboard
from aiogram.types import ReplyKeyboardRemove, CallbackQuery


@dp.message_handler(state=UserState.fullname)
async def fullname(message:  types.Message, state: FSMContext):
    full_name = message.text
    await state.update_data({"fullname": full_name}
    )
    await message.answer("Iltimos, tug'ilgan yilingizni kiriting! kun/oy/yil")
    await UserState.date_of_birth.set()


@dp.message_handler(state=UserState.date_of_birth)
async def dateofbirth(message: types.Message, state: FSMContext):
    date_of_birth = message.text
    await state.update_data({"date_of_birth": date_of_birth}
    )
    await message.answer("Iltimos, telefon raqamingizni jo'nating!\n \nYoki 'jo'natish' tugmasi orqali, yoki o'zingiz qo'lda kiriting!  \nMasalan, +998xx xxx xx xx", reply_markup=UserKeyboard.phone_number)
    await UserState.phone_number.set()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=UserState.phone_number)
async def phone_number(message: types.Message, state: FSMContext):
    contact = message.contact.phone_number
    user_name = message.from_user.username
    telegram_id = message.from_user.id
    await state.update_data({'phone_number': contact, "username": user_name, "telegram_id": telegram_id})
    await message.answer("Which grade / course are you in or graduated ? \nNechinchi sinf / kursda o'qiysiz yoki bitirganmisiz?", reply_markup=ReplyKeyboardRemove(selective=True))
    await UserState.grade.set()

phone_number_regexp = "^[+]998[389][012345789][0-9]{7}$"

@dp.message_handler(regexp=phone_number_regexp, state=UserState.phone_number)
async def phone(message: types.Message, state: FSMContext):
    phone_number = message.text
    username = message.from_user.username
    telegram_id = message.from_user.id
    await state.update_data({'phone_number': phone_number, "username": username, "telegram_id": telegram_id})
    await message.answer("Which grade / course  are you in or graduated ? \nNechinchi sinf / kursda o'qiysiz yoki bitirganmisiz ?", reply_markup=ReplyKeyboardRemove(selective=True))
    await UserState.grade.set()


@dp.message_handler(state=UserState.phone_number)
async def phone(message: types.Message):
    await message.answer("Iltimos, to'g'ri formatdagi raqam kiriting!")
    await UserState.phone_number.set()