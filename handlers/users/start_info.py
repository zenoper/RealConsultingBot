from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from states.userStates import B1orF1States, B1UserState
from keyboards.default import UserKeyboard, B12UserKeyboard
from states.userStates import UserState, ResultState, F1UserState, CanadaUserState, EuropeUserState


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
            await message.answer(
                "O'zbekistonda istiqomat qilasizmi yoki chet-eldami? \n\nDo you live in Uzbekistan or abroad?",
                reply_markup=UserKeyboard.intorlocal)
            await UserState.interORlocal.set()
    else:
        await message.answer(
            "Iltimos, telegram profilingizga username qo'shing. \nShunda sizga aloqaga chiqa olamiz. \n\nPlease, add a username to your telegram profile. Then, we can contact you!")


@dp.message_handler(content_types=types.ContentTypes.ANY, state=UserState.date_of_birth)
async def dateofbirth(message: types.Message):
    await message.answer("Iltimos, faqatgina harflardan foydalaning! \n\nPlease, only use letters!")


@dp.message_handler(text="O'zbekistonda | In Uzbekistan", content_types=types.ContentTypes.TEXT, state=UserState.interORlocal)
async def intorlocal(message: types.Message):
    await message.answer(
        "Iltimos, telefon raqamingizni jo'nating! \n<b>'jo'natish'</b> tugmasini bosing yoki o'zingiz kiriting! \nMasalan, +998xx xxx xx xx \n\nPlease, send your phone number! \nEither press <b>'send'</b> button or fill in yourself! \nFor example, +998xx xxx xx xx",
        reply_markup=UserKeyboard.phone_number)
    await UserState.phone_number.set()


@dp.message_handler(text="Chet-elda | Abroad", content_types=types.ContentTypes.TEXT, state=UserState.interORlocal)
async def intorlocal(message: types.Message):
    await message.answer(
        "Iltimos, telefon raqamingizni jo'nating! \n<b>'jo'natish'</b> tugmasini bosing yoki o'zingiz kiriting!\n\nPlease, send your phone number! \nEither press <b>'send'</b> button or fill in yourself!",
        reply_markup=UserKeyboard.phone_number)
    await UserState.phone_number_int.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=UserState.interORlocal)
async def intorlocal(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing! \n\nPlease, click one of the buttons!", reply_markup=UserKeyboard.intorlocal)


@dp.message_handler(content_types=types.ContentType.CONTACT, state=UserState.phone_number)
@dp.message_handler(content_types=types.ContentType.CONTACT, state=UserState.phone_number_int)
async def phone_number(message: types.Message, state: FSMContext):
    contact = message.contact.phone_number
    user_name = message.from_user.username
    telegram_id = message.from_user.id
    await state.update_data({'phone_number': contact, "username": user_name, "telegram_id": telegram_id})
    await message.answer("Qaysi turdagi visani olmoqchisiz?", reply_markup=UserKeyboard.b1orf1)
    await B1orF1States.start.set()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=UserState.phone_number_int)
async def phone(message: types.Message, state: FSMContext):
    phonenumber = message.text
    telegram_id = message.from_user.id
    await state.update_data({'phone_number': phonenumber, "telegram_id": telegram_id})
    await message.answer("Qaysi turdagi visani olmoqchisiz?", reply_markup=UserKeyboard.b1orf1)
    await B1orF1States.start.set()

@dp.message_handler(content_types=types.ContentTypes.ANY, state=UserState.phone_number_int)
async def dateofbirth(message: types.Message):
    await message.answer("Iltimos, faqatgina raqamlardan foydalaning! \n\nPlease, only use numbers!")

phone_number_regexp = "^[+]998[389][012345789][0-9]{7}$"

@dp.message_handler(regexp=phone_number_regexp, content_types=types.ContentTypes.TEXT, state=UserState.phone_number)
async def phone(message: types.Message, state: FSMContext):
    phonenumber = message.text
    telegram_id = message.from_user.id
    await state.update_data({'phone_number': phonenumber, "telegram_id": telegram_id})
    await message.answer("Qaysi turdagi visani olmoqchisiz?", reply_markup=UserKeyboard.b1orf1)
    await B1orF1States.start.set()

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=UserState.phone_number)
async def phone(message: types.Message):
    await message.answer("Iltimos, to'g'ri formatdagi raqam kiriting!", reply_markup=UserKeyboard.phone_number)

@dp.message_handler(content_types=types.ContentTypes.ANY, state=UserState.phone_number)
async def dateofbirth(message: types.Message):
    await message.answer("Iltimos, faqatgina raqamlardan foydalaning! \n\nPlease, only use numbers!")



@dp.message_handler(state=B1orF1States.start, text="🇺🇸 F1 STUDENT VISA")
async def start(message: types.Message):
    await message.answer("Tanlang: \n\nChoose one:", reply_markup=UserKeyboard.grade)
    await F1UserState.grade.set()


@dp.message_handler(state=B1orF1States.start, text="🇺🇸 B1/B2 SAYOHAT VISA")
async def start(message: types.Message):
    await message.answer("Chet-elda oldin bo'lganmisiz? \n\nHave you been aboard?",
                         reply_markup=B12UserKeyboard.abroad)
    await B1UserState.abroad.set()


@dp.message_handler(state=B1orF1States.start, text="🇨🇦 SAYOHAT VISA")
async def start(message: types.Message):
    await message.answer("Chet-elda oldin bo'lganmisiz? \n\nHave you been aboard?",
                         reply_markup=B12UserKeyboard.abroad)
    await CanadaUserState.abroad.set()


@dp.message_handler(state=B1orF1States.start, text="🇪🇺 SAYOHAT VISA")
async def start(message: types.Message):
    await message.answer("Chet-elda oldin bo'lganmisiz? \n\nHave you been aboard?",
                         reply_markup=B12UserKeyboard.abroad)
    await EuropeUserState.abroad.set()


@dp.message_handler(state=B1orF1States, content_types=types.ContentTypes.ANY)
async def start(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing!", reply_markup=UserKeyboard.b1orf1)
