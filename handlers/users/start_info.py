from aiogram import F, types
from aiogram.filters import StateFilter
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from loader import dp, db, bot
from states.userStates import B1orF1States, B1UserState
from keyboards.default import UserKeyboard, B12UserKeyboard
from states.userStates import UserState, ResultState, F1UserState, CanadaUserState, EuropeUserState


@dp.message(StateFilter(UserState.fullname), F.content_type == ContentType.TEXT)
async def fullname(message: types.Message, state: FSMContext):
    full_name = message.text
    if len(full_name) <= 5:
        await message.answer(
            "Iltimos, ism va familiyangizni <b>to'liq</b> kiriting! \n\nPlease, fill in your name and surname <b>completely</b>!")
    else:
        await state.update_data({"fullname": full_name})
        await state.update_data({"qualification": 0})
        await message.answer("Iltimos, tug'ilgan kun, oy, va yilingizni kiriting! \n\nPlease, fill in your birthdate!")
        await state.set_state(UserState.date_of_birth)


@dp.message(StateFilter(UserState.fullname))
async def fullname(message: types.Message):
    await message.answer("Iltimos, faqatgina harflardan foydalaning! \n\nPlease, only use letters!")


@dp.message(StateFilter(UserState.date_of_birth), F.content_type == ContentType.TEXT)
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
            await message.answer(
                "O'zbekistonda istiqomat qilasizmi yoki chet-eldami? \n\nDo you live in Uzbekistan or abroad?",
                reply_markup=UserKeyboard.intorlocal)
            await state.set_state(UserState.interORlocal)
    else:
        await message.answer(
            "Iltimos, telegram profilingizga username qo'shing. \nShunda sizga aloqaga chiqa olamiz. \n\nPlease, add a username to your telegram profile. Then, we can contact you!")


@dp.message(StateFilter(UserState.date_of_birth))
async def dateofbirth(message: types.Message):
    await message.answer("Iltimos, faqatgina harflardan foydalaning! \n\nPlease, only use letters!")


@dp.message(StateFilter(UserState.interORlocal), F.text == "O'zbekistonda | In Uzbekistan")
async def intorlocal(message: types.Message, state: FSMContext):
    await message.answer(
        "Iltimos, telefon raqamingizni jo'nating! \n<b>'jo'natish'</b> tugmasini bosing yoki o'zingiz kiriting! \nMasalan, +998xx xxx xx xx \n\nPlease, send your phone number! \nEither press <b>'send'</b> button or fill in yourself! \nFor example, +998xx xxx xx xx",
        reply_markup=UserKeyboard.phone_number)
    await state.set_state(UserState.phone_number)


@dp.message(StateFilter(UserState.interORlocal), F.text == 'Chet-elda | Abroad')
async def intorlocal(message: types.Message, state: FSMContext):
    await message.answer(
        "Iltimos, telefon raqamingizni jo'nating! \n<b>'jo'natish'</b> tugmasini bosing yoki o'zingiz kiriting!\n\nPlease, send your phone number! \nEither press <b>'send'</b> button or fill in yourself!",
        reply_markup=UserKeyboard.phone_number)
    await state.set_state(UserState.phone_number_int)


@dp.message(StateFilter(UserState.interORlocal))
async def intorlocal(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing! \n\nPlease, click one of the buttons!", reply_markup=UserKeyboard.intorlocal)


@dp.message(StateFilter(UserState.phone_number), F.content_type == ContentType.CONTACT)
@dp.message(StateFilter(UserState.phone_number_int), F.content_type == ContentType.CONTACT)
async def phone_number(message: types.Message, state: FSMContext):
    contact = message.contact.phone_number
    user_name = message.from_user.username
    telegram_id = message.from_user.id
    await state.update_data({'phone_number': contact, "username": user_name, "telegram_id": telegram_id})
    await message.answer("Tanlang: \n\nChoose one:", reply_markup=UserKeyboard.grade)
    await state.set_state(F1UserState.grade)


@dp.message(StateFilter(UserState.phone_number_int), F.content_type == ContentType.TEXT)
async def phone(message: types.Message, state: FSMContext):
    phonenumber = message.text
    telegram_id = message.from_user.id
    await state.update_data({'phone_number': phonenumber, "telegram_id": telegram_id})
    await message.answer("Tanlang: \n\nChoose one:", reply_markup=UserKeyboard.grade)
    await state.set_state(F1UserState.grade)

@dp.message(StateFilter(UserState.phone_number_int))
async def dateofbirth(message: types.Message):
    await message.answer("Iltimos, faqatgina raqamlardan foydalaning! \n\nPlease, only use numbers!")

phone_number_regexp = "^[+]998[389][012345789][0-9]{7}$"

@dp.message(StateFilter(UserState.phone_number), F.content_type == ContentType.TEXT, F.text.regexp(phone_number_regexp))
async def phone(message: types.Message, state: FSMContext):
    phonenumber = message.text
    telegram_id = message.from_user.id
    await state.update_data({'phone_number': phonenumber, "telegram_id": telegram_id})
    await message.answer("Tanlang: \n\nChoose one:", reply_markup=UserKeyboard.grade)
    await state.set_state(F1UserState.grade)

@dp.message(StateFilter(UserState.phone_number), F.content_type == ContentType.TEXT)
async def phone(message: types.Message):
    await message.answer("Iltimos, to'g'ri formatdagi raqam kiriting!", reply_markup=UserKeyboard.phone_number)

@dp.message(StateFilter(UserState.phone_number))
async def dateofbirth(message: types.Message):
    await message.answer("Iltimos, faqatgina raqamlardan foydalaning! \n\nPlease, only use numbers!")



@dp.message(StateFilter(B1orF1States.start), F.text == '🇺🇸 F1 STUDENT VISA')
async def start(message: types.Message, state: FSMContext):
    await message.answer("Tanlang: \n\nChoose one:", reply_markup=UserKeyboard.grade)
    await state.set_state(F1UserState.grade)


@dp.message(StateFilter(B1orF1States.start), F.text == '🇺🇸 B1/B2 SAYOHAT VISA')
async def start(message: types.Message, state: FSMContext):
    await message.answer("Chet-elda oldin bo'lganmisiz? \n\nHave you been aboard?",
                         reply_markup=B12UserKeyboard.abroad)
    await state.set_state(B1UserState.abroad)


@dp.message(StateFilter(B1orF1States.start), F.text == '🇨🇦 SAYOHAT VISA')
async def start(message: types.Message, state: FSMContext):
    await message.answer("Chet-elda oldin bo'lganmisiz? \n\nHave you been aboard?",
                         reply_markup=B12UserKeyboard.abroad)
    await state.set_state(CanadaUserState.abroad)


@dp.message(StateFilter(B1orF1States.start), F.text == '🇪🇺 SAYOHAT VISA')
async def start(message: types.Message, state: FSMContext):
    await message.answer("Chet-elda oldin bo'lganmisiz? \n\nHave you been aboard?",
                         reply_markup=B12UserKeyboard.abroad)
    await state.set_state(EuropeUserState.abroad)


@dp.message(StateFilter(B1orF1States))
async def start(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing!", reply_markup=UserKeyboard.b1orf1)
