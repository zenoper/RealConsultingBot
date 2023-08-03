from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from states.userStates import UserState, GradeStates, TestStates
from keyboards.default import UserKeyboard
from aiogram.types import ReplyKeyboardRemove


@dp.message_handler(state=UserState.fullname)
async def fullname(message:  types.Message, state: FSMContext):
    full_name = message.text
    await state.update_data({"fullname": full_name})
    await message.answer("Iltimos, tug'ilgan yilingizni <b>kun/oy/yil</b> formatida kiriting! \n\nPlease, fill in your birthdate in <b>dd/mm/yyyy</b> format!")
    await UserState.date_of_birth.set()

birth_date_regexp = "^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$"

@dp.message_handler(regexp=birth_date_regexp, state=UserState.date_of_birth)
async def dateofbirth(message: types.Message, state: FSMContext):
    date_of_birth = message.text
    await state.update_data({"date_of_birth": date_of_birth})
    await message.answer("Iltimos, telefon raqamingizni jo'nating! \n<b>'jo'natish'</b> tugmasini bosing yoki o'zingiz kiriting! \nMasalan, +998xx xxx xx xx \n\nPlease, send your phone number! \nEither press <b>'send'</b> button or fill in yourself! \nFor example, +998xx xxx xx xx", reply_markup=UserKeyboard.phone_number)
    await UserState.phone_number.set()


@dp.message_handler(state=UserState.date_of_birth)
async def dateofbirth(message: types.Message):
    await message.answer("Iltimos, faqatgina to'g'ri <b>kun/oy/yil</b> formatida kiriting! \n\nPlease, fill in your birthdate only in the correct <b>dd/mm/yyyy</b> format!")


@dp.message_handler(content_types=types.ContentType.CONTACT, state=UserState.phone_number)
async def phone_number(message: types.Message, state: FSMContext):
    contact = message.contact.phone_number
    user_name = message.from_user.username
    telegram_id = message.from_user.id
    await state.update_data({'phone_number': contact, "username": user_name, "telegram_id": telegram_id})
    await message.answer("Tanlang: \n\nChoose one:", reply_markup=UserKeyboard.grade)
    await UserState.grade.set()

phone_number_regexp = "^[+]998[389][012345789][0-9]{7}$"

@dp.message_handler(regexp=phone_number_regexp, state=UserState.phone_number)
async def phone(message: types.Message, state: FSMContext):
    phonenumber = message.text
    username = message.from_user.username
    telegram_id = message.from_user.id
    await state.update_data({'phone_number': phonenumber, "username": username, "telegram_id": telegram_id})
    await message.answer("Tanlang: \n\nChoose one:", reply_markup=UserKeyboard.grade)
    await UserState.grade.set()


@dp.message_handler(state=UserState.phone_number)
async def phone(message: types.Message):
    await message.answer("Iltimos, to'g'ri formatdagi raqam kiriting!")
    await UserState.phone_number.set()


@dp.message_handler(text="Maktabda o'qiyman | At high school", state=UserState.grade)
async def school(message: types.Message):
    await message.answer("Nechinchi sinfda o'qiysiz? \n\nWhat grade at high school are you in?", reply_markup=UserKeyboard.school)
    await GradeStates.school.set()


@dp.message_handler(state=GradeStates.school)
async def school(message: types.Message, state: FSMContext):
    grade = message.text
    await state.update_data({'grade': f"{grade} sinf"})
    await message.answer("Qaysi darajada o'qimoqchisiz? Tanlang: \n\nWhat degree do you want to study at? Choose one:", reply_markup=UserKeyboard.degree)
    await UserState.degree.set()


@dp.message_handler(text="Maktabni bitirganman | In a gap year", state=UserState.grade)
async def school(message: types.Message, state: FSMContext):
    await state.update_data({"grade": "maktabni bitirgan/gap year"})
    await message.answer("Qaysi darajada o'qimoqchisiz? Tanlang: \n\nWhat degree do you want to study at? Choose one:", reply_markup=UserKeyboard.degree)
    await UserState.degree.set()


@dp.message_handler(text="Universitetda o'qiyman | At university", state=UserState.grade)
async def university(message: types.Message):
    await message.answer("Nechinchi kursda o'qiysiz? \n\nWhat year at university are you in?", reply_markup=UserKeyboard.university)
    await GradeStates.university.set()


@dp.message_handler(state=GradeStates.university)
async def university(message: types.Message, state: FSMContext):
    year = message.text
    await state.update_data({"grade": f"{year} kurs/year"})
    await message.answer("Qaysi darajada o'qimoqchisiz? Tanlang: \n\nWhat degree do you want to study at? Choose one:", reply_markup=UserKeyboard.degree)
    await UserState.degree.set()


@dp.message_handler(text="Bakalavr | Bachelor's", state=UserState.degree)
async def degree(message: types.Message, state: FSMContext):
    await state.update_data({"degree": "bachelor's"})
    await message.answer("Sizda IELTS yoki Duolingo bormi? \nNatijasi yuqorisini tanlang! \n\nDo you have IELTS or Duolingo score? \nChoose the one you have highest score from!", reply_markup=UserKeyboard.test_score)
    await UserState.test_score.set()


@dp.message_handler(text="Magistratura | Master's", state=UserState.degree)
async def degree(message: types.Message, state: FSMContext):
    await state.update_data({"degree": "master's"})
    await message.answer("Sizda IELTS yoki Duolingo bormi? \nNatijasi yuqorisini tanlang! \n\nDo you have IELTS or Duolingo score? \nChoose the one you have highest score from!", reply_markup=UserKeyboard.test_score)
    await UserState.test_score.set()


@dp.message_handler(state=UserState.degree)
async def degree(message: types.Message, state: FSMContext):
    await message.answer("Iltimos, tugmalardan birini bosing! \nPlease, click one of the buttons!", reply_markup=UserKeyboard.test_score)
    await UserState.test_score.set()

@dp.message_handler(text="IELTS", state=UserState.test_score)
async def test_score(message: types.Message):
    await message.answer("IELTS balingiz nechchi? \n\nWhat is your IELTS score?")
    await TestStates.ielts.set()


@dp.message_handler(state=TestStates.ielts)
async def ielts(message: types.Message, state: FSMContext):
    ielts_of = message.text
    await state.update_data({"test_score": f"IELTS {ielts_of}"})

    data = await state.get_data()
    full_name = data.get("fullname")
    date_of_birth = data.get("date_of_birth")
    contact_number = data.get("phone_number")
    grade = data.get("grade")
    degree_of = data.get("degree")
    test_score_of = data.get("test_score")

    msg = "Iltimos, shaxsiy ma'lumotingiz to'g'riligini tasdiqlang! \nPlease, confirm your personal info is correct! \n \n"
    msg += f"To'liq ism/Full name - <b>{full_name}</b> \n\n"
    msg += f"Tug'ilgan yilingiz/Date of birth - <b>{date_of_birth}</b> \n\n"
    msg += f"Telefon raqamingiz/Phone Number - <b>{contact_number}</b> \n\n"
    msg += f"O'quv yilingiz/Study year - <b>{grade}</b> \n\n"
    msg += f"Tanlangan daraja/Chosen degree - <b>{degree_of}</b> \n\n"
    msg += f"Test natijangiz/Test score - <b>{test_score_of}</b>"

    await message.answer(msg, reply_markup=UserKeyboard.confirmation)
    await UserState.confirmation.set()


@dp.message_handler(text="Duolingo", state=UserState.test_score)
async def test_score(message: types.Message):
    await message.answer("Duolingo balingiz nechchi? \n\nWhat is your Duolingo score?")
    await TestStates.duolingo.set()


@dp.message_handler(state=TestStates.duolingo)
async def ielts(message: types.Message, state: FSMContext):
    duolingo_of = message.text
    await state.update_data({"test_score": f"Duolingo {duolingo_of}"})

    data = await state.get_data()
    full_name = data.get("fullname")
    date_of_birth = data.get("date_of_birth")
    contact_number = data.get("phone_number")
    grade = data.get("grade")
    degree_of = data.get("degree")
    test_score_of = data.get("test_score")

    msg = "Iltimos, shaxsiy ma'lumotingiz to'g'riligini tasdiqlang! \nPlease, confirm your personal info is correct! \n \n"
    msg += f"To'liq ism/Full name - <b>{full_name}</b> \n\n"
    msg += f"Tug'ilgan yilingiz/Date of birth - <b>{date_of_birth}</b> \n\n"
    msg += f"Telefon raqamingiz/Phone Number - <b>{contact_number}</b> \n\n"
    msg += f"O'quv yilingiz/Study year - <b>{grade}</b> \n\n"
    msg += f"Tanlangan daraja/Chosen degree - <b>{degree_of}</b> \n\n"
    msg += f"Test natijangiz/Test score - <b>{test_score_of}</b>"

    await message.answer(msg, reply_markup=UserKeyboard.confirmation)
    await UserState.confirmation.set()


@dp.message_handler(text="Yo'q/None", state=UserState.test_score)
async def test_score(message: types.Message, state: FSMContext):
    await state.update_data({"test_score": "Yo'q/None"})

    data = await state.get_data()
    full_name = data.get("fullname")
    date_of_birth = data.get("date_of_birth")
    contact_number = data.get("phone_number")
    grade = data.get("grade")
    degree_of = data.get("degree")
    test_score_of = data.get("test_score")

    msg = "Iltimos, shaxsiy ma'lumotingiz to'g'riligini tasdiqlang! \nPlease, confirm your personal info is correct! \n \n"
    msg += f"To'liq ism/Full name - <b>{full_name}</b> \n\n"
    msg += f"Tug'ilgan yilingiz/Date of birth - <b>{date_of_birth}</b> \n\n"
    msg += f"Telefon raqamingiz/Phone Number - <b>{contact_number}</b> \n\n"
    msg += f"O'quv yilingiz/Study year - <b>{grade}</b> \n\n"
    msg += f"Tanlangan daraja/Chosen degree - <b>{degree_of}</b> \n\n"
    msg += f"Test natijangiz/Test score - <b>{test_score_of}</b>"

    await message.answer(msg, reply_markup=UserKeyboard.confirmation)
    await UserState.confirmation.set()


@dp.message_handler(text="Tasdiqlash/Confirm! ✅", state=UserState.confirmation)
async def confirmation(message: types.Message):
    await message.answer("Hamkorligingiz uchun rahmat!\nIltimos, sizga aloqaga chiqishimizni kuting! \n\nThank you for cooperation! \nPlease, wait for us to get in touch with you! 🙂", reply_markup=ReplyKeyboardRemove(selective=True))
    await UserState.waiting.set()


@dp.message_handler(text="Tahrirlash/Edit ✏️", state=UserState.confirmation)
async def edit(message: types.Message):
    await message.answer("Iltimos, to'liq ismingizni kiriting! \n\nPlease, fill in your full name!")
    await UserState.fullname.set()
