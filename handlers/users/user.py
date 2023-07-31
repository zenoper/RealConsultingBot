from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from states.userStates import UserState, GradeStates

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
    await message.answer("Which grade / course are you in or graduated ? \nNechinchi sinf / kursda o'qiysiz yoki bitirganmisiz?", reply_markup=UserKeyboard.grade)
    await UserState.grade.set()

phone_number_regexp = "^[+]998[389][012345789][0-9]{7}$"

@dp.message_handler(regexp=phone_number_regexp, state=UserState.phone_number)
async def phone(message: types.Message, state: FSMContext):
    phone_number = message.text
    username = message.from_user.username
    telegram_id = message.from_user.id
    await state.update_data({'phone_number': phone_number, "username": username, "telegram_id": telegram_id})
    await message.answer("Which grade / course  are you in or graduated ? \nNechinchi sinf / kursda o'qiysiz yoki bitirganmisiz ?", reply_markup=UserKeyboard.grade)
    await UserState.grade.set()


@dp.message_handler(state=UserState.phone_number)
async def phone(message: types.Message):
    await message.answer("Iltimos, to'g'ri formatdagi raqam kiriting!")
    await UserState.phone_number.set()


@dp.message_handler(text="Maktabda o'qiyman", state=UserState.grade)
async def school(message: types.Message):
    await message.answer("Nechinchi sinfda o'qiysiz?", reply_markup=UserKeyboard.school)
    await GradeStates.school.set()

@dp.message_handler(state=GradeStates.school)
async def school(message: types.Message, state: FSMContext):
    grade = message.text
    await state.update_data({'grade': f"{grade} sinf"})
    await message.answer("Tanlang:", reply_markup=UserKeyboard.degree)
    await UserState.degree.set()

@dp.message_handler(text="Maktabni bitirganman", state=UserState.grade)
async def school(message: types.Message, state: FSMContext):
    await state.update_data({"grade": "maktabni bitirgan"})
    await message.answer("Tanlang:", reply_markup=UserKeyboard.degree)
    await UserState.degree.set()

@dp.message_handler(text="Universitetda o'qiyman", state=UserState.grade)
async def university(message: types.Message):
    await message.answer("Nechinchi kursda o'qiysiz?", reply_markup=UserKeyboard.university)
    await GradeStates.university.set()

@dp.message_handler(state=GradeStates.university)
async def university(message: types.Message, state: FSMContext):
    grade = message.text
    await state.update_data({"grade": f"{grade} kurs"})
    await message.answer("Tanlang:", reply_markup=UserKeyboard.degree)
    await UserState.degree.set()

@dp.message_handler(state=UserState.degree)
async def degree(message: types.Message, state: FSMContext):
    degree = message.text
    await state.update_data({"degree": degree})
    await message.answer("What is your IELTS / Duolingo Score ?")
    await UserState.test_score.set()

@dp.message_handler(state=UserState.test_score)
async def test_score(message: types.Message, state: FSMContext):
    test_score = message.text
    await state.update_data({"test_score": test_score})
    await message.answer("TO BE CONTINUED!")
    await UserState.confirmation.set()