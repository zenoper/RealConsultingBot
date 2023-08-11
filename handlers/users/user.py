import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from states.userStates import UserState, GradeStates, TestStates
from keyboards.default import UserKeyboard
from aiogram.types import ReplyKeyboardRemove
from data.config import ADMINS
import re


@dp.message_handler(state=UserState.fullname)
async def fullname(message:  types.Message, state: FSMContext):
    full_name = message.text
    if len(full_name) <= 5:
        await message.answer("Iltimos, ism va familiyangizni <b>to'liq</b> kiriting! \n\nPlease, fill in your name and surname <b>completely</b>!")
    else:
        await state.update_data({"fullname": full_name})
        await message.answer("Iltimos, tug'ilgan kun, oy, va yilingizni kiriting! \n\nPlease, fill in your birthdate!")
        await UserState.date_of_birth.set()
@dp.message_handler(content_types=types.ContentTypes.ANY, state=UserState.fullname)
async def fullname(message: types.Message):
    await message.answer("Iltimos, faqatgina harflardan foydalaning! \n\nPlease, only use letters!")


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=UserState.date_of_birth)
async def dateofbirth(message: types.Message, state: FSMContext):
    date_of_birth = message.text
    if len(date_of_birth) <= 5:
        await message.answer("Iltimos, tug'ilgan kun, oy, va yilingizni <b>to'liq</b> kiriting! \n\nPlease, fill in your <b>complete</b> birthdate!")
    else:
        await state.update_data({"date_of_birth": date_of_birth})
        await message.answer("Iltimos, telefon raqamingizni jo'nating! \n<b>'jo'natish'</b> tugmasini bosing yoki o'zingiz kiriting! \nMasalan, +998xx xxx xx xx \n\nPlease, send your phone number! \nEither press <b>'send'</b> button or fill in yourself! \nFor example, +998xx xxx xx xx", reply_markup=UserKeyboard.phone_number)
        await UserState.phone_number.set()
@dp.message_handler(content_types=types.ContentTypes.ANY, state=UserState.date_of_birth)
async def dateofbirth(message: types.Message):
    await message.answer("Iltimos, faqatgina harflardan foydalaning! \n\nPlease, only use letters!")

@dp.message_handler(content_types=types.ContentType.CONTACT, state=UserState.phone_number)
async def phone_number(message: types.Message, state: FSMContext):
    contact = message.contact.phone_number
    user_name = message.from_user.username
    telegram_id = message.from_user.id
    await state.update_data({'phone_number': contact, "username": user_name, "telegram_id": telegram_id})
    await message.answer("Tanlang: \n\nChoose one:", reply_markup=UserKeyboard.grade)
    await UserState.grade.set()

phone_number_regexp = "^[+]998[389][012345789][0-9]{7}$"
@dp.message_handler(regexp=phone_number_regexp, content_types=types.ContentTypes.TEXT, state=UserState.phone_number)
async def phone(message: types.Message, state: FSMContext):
    phonenumber = message.text
    username = message.from_user.username
    telegram_id = message.from_user.id
    await state.update_data({'phone_number': phonenumber, "username": username, "telegram_id": telegram_id})
    await message.answer("Tanlang: \n\nChoose one:", reply_markup=UserKeyboard.grade)
    await UserState.grade.set()
@dp.message_handler(content_types=types.ContentTypes.TEXT, state=UserState.phone_number)
async def phone(message: types.Message):
    await message.answer("Iltimos, to'g'ri formatdagi raqam kiriting!", reply_markup=UserKeyboard.phone_number)
    await UserState.phone_number.set()
@dp.message_handler(content_types=types.ContentTypes.ANY, state=UserState.phone_number)
async def dateofbirth(message: types.Message):
    await message.answer("Iltimos, faqatgina raqamlardan foydalaning! \n\nPlease, only use numbers!")


@dp.message_handler(text="Maktabda o'qiyman | At high school", content_types=types.ContentTypes.TEXT, state=UserState.grade)
async def school(message: types.Message):
    await message.answer("Nechinchi sinfda o'qiysiz? \n\nWhat grade at high school are you in?", reply_markup=UserKeyboard.school)
    await GradeStates.school.set()
@dp.message_handler(text="9", content_types=types.ContentTypes.TEXT, state=GradeStates.school)
@dp.message_handler(text="10", content_types=types.ContentTypes.TEXT, state=GradeStates.school)
@dp.message_handler(text="11", content_types=types.ContentTypes.TEXT, state=GradeStates.school)
async def school(message: types.Message, state: FSMContext):
    grade = message.text
    await state.update_data({'grade': f"{grade} sinf"})
    await message.answer("Qaysi darajada o'qimoqchisiz? Tanlang: \n\nWhat degree do you want to study at? Choose one:", reply_markup=UserKeyboard.degree)
    await UserState.degree.set()
@dp.message_handler(content_types=types.ContentTypes.ANY, state=GradeStates.school)
async def school(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing! \nPlease, click one of the buttons!", reply_markup=UserKeyboard.school)


@dp.message_handler(text="Maktabni bitirganman | In a gap year", content_types=types.ContentTypes.TEXT, state=UserState.grade)
async def school(message: types.Message, state: FSMContext):
    await state.update_data({"grade": "maktabni bitirgan/gap year"})
    await message.answer("Qaysi darajada o'qimoqchisiz? Tanlang: \n\nWhat degree do you want to study at? Choose one:", reply_markup=UserKeyboard.degree)
    await UserState.degree.set()

@dp.message_handler(text="Universitetda o'qiyman | At university", content_types=types.ContentTypes.TEXT, state=UserState.grade)
async def university(message: types.Message):
    await message.answer("Nechinchi kursda o'qiysiz? \n\nWhat year at university are you in?", reply_markup=UserKeyboard.university)
    await GradeStates.university.set()
@dp.message_handler(text="1", content_types=types.ContentTypes.TEXT, state=GradeStates.university)
@dp.message_handler(text="2", content_types=types.ContentTypes.TEXT, state=GradeStates.university)
@dp.message_handler(text="3", content_types=types.ContentTypes.TEXT, state=GradeStates.university)
@dp.message_handler(text="4", content_types=types.ContentTypes.TEXT, state=GradeStates.university)
async def university(message: types.Message, state: FSMContext):
    year = message.text
    await state.update_data({"grade": f"{year} kurs/year"})
    await message.answer("Qaysi darajada o'qimoqchisiz? Tanlang: \n\nWhat degree do you want to study at? Choose one:", reply_markup=UserKeyboard.degree)
    await UserState.degree.set()
@dp.message_handler(content_types=types.ContentTypes.ANY, state=GradeStates.university)
async def school(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing! \nPlease, click one of the buttons!", reply_markup=UserKeyboard.university)

@dp.message_handler(content_types=types.ContentTypes.ANY, state=UserState.grade)
async def grade(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing! \n\nPlease, click one of the buttons!", reply_markup=UserKeyboard.grade)


@dp.message_handler(text="Bakalavr | Bachelor's", content_types=types.ContentTypes.TEXT, state=UserState.degree)
async def degree(message: types.Message, state: FSMContext):
    await state.update_data({"degree": "bachelor's"})
    await message.answer("Sizda IELTS yoki Duolingo bormi? \nNatijasi yuqorisini tanlang! \n\nDo you have IELTS or Duolingo score? \nChoose the one you have highest score from!", reply_markup=UserKeyboard.test_score)
    await UserState.test_score.set()
@dp.message_handler(text="Magistratura | Master's", content_types=types.ContentTypes.TEXT, state=UserState.degree)
async def degree(message: types.Message, state: FSMContext):
    await state.update_data({"degree": "master's"})
    await message.answer("Sizda IELTS yoki Duolingo bormi? \nNatijasi yuqorisini tanlang! \n\nDo you have IELTS or Duolingo score? \nChoose the one you have highest score from!", reply_markup=UserKeyboard.test_score)
    await UserState.test_score.set()
@dp.message_handler(content_types=types.ContentTypes.ANY, state=UserState.degree)
async def degree(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing! \nPlease, click one of the buttons!", reply_markup=UserKeyboard.degree)


@dp.message_handler(text="IELTS", content_types=types.ContentTypes.TEXT, state=UserState.test_score)
async def test_score(message: types.Message):
    await message.answer("IELTS balingiz nechchi? \n\nWhat is your IELTS score?")
    await TestStates.ielts.set()

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=TestStates.ielts)
async def ielts(message: types.Message, state: FSMContext):
    ielts_of = message.text
    if message.text.isdigit() or is_float(message.text):
        if len(ielts_of) < 4:
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
        else:
            await message.answer("Javobingiz 3 xonadan oshmasligi kerak! \nMasalan: <b>6.5</b>  \n\nYour response can't have more than 3 characters! \nFor example: <b>6</b>")
    else:
        await message.answer("Iltimos, IELTS natijangizni to'g'ri formatda kiriting! \nMasalan: <b>6.5</b>  \n\nPlease, write your IELTS score in the correct format! \nFor example: <b>6</b>")

@dp.message_handler(content_types=types.ContentTypes.ANY, state=TestStates.ielts)
async def ielts(message: types.Message):
    await message.answer("Iltimos, faqat raqamlardan foydalananing! \n\nPLease, only use numbers!")


@dp.message_handler(text="Duolingo", content_types=types.ContentTypes.TEXT, state=UserState.test_score)
async def test_score(message: types.Message):
    await message.answer("Duolingo balingiz nechchi? \n\nWhat is your Duolingo score?")
    await TestStates.duolingo.set()


@dp.message_handler(lambda message: message.text.isdigit(), content_types=types.ContentTypes.TEXT, state=TestStates.duolingo)
async def ielts(message: types.Message, state: FSMContext):
    duolingo_of = message.text
    if len(duolingo_of) < 4:
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
    else:
        await message.answer("Javobingiz 3 xonadan oshmasligi kerak! \nMasalan: <b>135</b>  \n\nYour response can't have more than 3 characters! \nFor example: <b>125</b>")


@dp.message_handler(lambda message: not message.text.isdigit(), content_types=types.ContentTypes.TEXT, state=TestStates.duolingo)
async def ielts(message: types.Message):
    await message.answer("Iltimos, faqat raqamlardan foydalaning! \nMasalan: <b>135</b> \n\nPlease, only use numbers! \nFor example: <b>125</b>")
@dp.message_handler(content_types=types.ContentTypes.ANY, state=TestStates.duolingo)
async def ielts(message: types.Message):
    await message.answer("Iltimos, faqat raqamlardan foydalaning! \nMasalan: <b>135</b> \n\nPlease, only use numbers! \nFor example: <b>125</b>")


@dp.message_handler(text="Yo'q/None", content_types=types.ContentTypes.TEXT, state=UserState.test_score)
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

@dp.message_handler(content_types=types.ContentTypes.ANY, state=UserState.test_score)
async def score(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing! \nPlease, click one of the buttons!", reply_markup=UserKeyboard.test_score)


@dp.message_handler(text="Tasdiqlash/Confirm! ✅", content_types=types.ContentTypes.TEXT, state=UserState.confirmation)
async def confirmation(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    try:
        user = await db.add_user(
            full_name=user_data.get("fullname"),
            date_of_birth=user_data.get("date_of_birth"),
            phone_number=user_data.get("phone_number"),
            grade=user_data.get("grade"),
            education_degree=user_data.get("degree"),
            test_score=user_data.get("test_score"),
            username=user_data.get("username"),
            telegram_id=user_data.get("telegram_id")
        )
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=user_data.get("telegram_id"))

    count = await db.count_users()
    msg = f"User '{user[1]}' has been added to the database! We now have {count} users."
    await bot.send_message(chat_id=ADMINS[0], text=msg)

    await message.answer("Hamkorligingiz uchun rahmat! \nAgar bizni talablarimizga to'g'ri kelsangiz, sizga aloqaga chiqamiz. \n\nThank you for cooperation! \nIf you meet our requirements, we will reach out to you. 🙂", reply_markup=ReplyKeyboardRemove(selective=True))
    await state.finish()


@dp.message_handler(text="Tahrirlash/Edit ✏️", content_types=types.ContentTypes.TEXT, state=UserState.confirmation)
async def edit(message: types.Message):
    await message.answer("Iltimos, to'liq ismingizni kiriting! \n\nPlease, fill in your full name!")
    await UserState.fullname.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=UserState.confirmation)
async def confirmation(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing! \nPlease, click one of the buttons!", reply_markup=UserKeyboard.confirmation)

