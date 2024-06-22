import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from states.userStates import EuropeUserState, UserState
from keyboards.default import B12UserKeyboard, UserKeyboard
from aiogram.types import ReplyKeyboardRemove, ContentTypes
from data.config import ADMINS


@dp.message_handler(state=EuropeUserState.abroad, text="Yes/Ha")
async def abroad(message: types):
    await message.answer("Iltimos, siz bo'lgan davlatlar nomini yozib qoldiring")
    await EuropeUserState.countries.set()


@dp.message_handler(state=EuropeUserState.abroad, text="No/Yo'q")
async def abroad(message: types, state: FSMContext):
    await state.update_data({"countries": "No"})
    await message.answer("Rasmiy ish joyingiz bormi? \n\nDo you officially work?", reply_markup=B12UserKeyboard.relatives)
    await EuropeUserState.work.set()


@dp.message_handler(state=EuropeUserState.abroad, content_types=ContentTypes.ANY)
async def abroad(message: types):
    await message.answer("Iltimos, tugmalardan birini bosing! \n\nPlease, click one of the buttons",
                         reply_markup=B12UserKeyboard.abroad)


@dp.message_handler(state=EuropeUserState.countries, content_types=ContentTypes.TEXT)
async def country(message: types, state: FSMContext):
    countries = message.text
    await state.update_data({"countries": countries})
    await message.answer("U davlat(lar)da qachon bo'lgansiz? \nMasalan: Mart, 2021 \n\nWhen have you been there? \nFor example, March, 2021")
    await EuropeUserState.visit_date.set()


@dp.message_handler(state=EuropeUserState.countries, content_types=types.ContentTypes.ANY)
async def country(message: types):
    await message.answer("Iltimos, faqatgina text yozing! \n\nPlease, only write text!")


# @dp.message_handler(state=EuropeUserState.visit_date, content_types=types.ContentTypes.TEXT)
# async def visit(message: types, state: FSMContext):
#     visit_date = message.text
#     if len(visit_date) >= 3:
#         await state.update_data({"visit_date": visit_date})
#
#         data = await state.get_data()
#         full_name = data.get("fullname")
#         birthdate = data.get("date_of_birth")
#         phone_number = data.get("phone_number")
#         countries = data.get("countries")
#         visit_date = data.get("visit_date")
#
#         msg = "Iltimos, shaxsiy ma'lumotingiz to'g'riligini tasdiqlang! \nPlease, confirm your personal info is correct! \n \n"
#         msg += f"To'liq ism/Full name - <b>{full_name}</b> \n\n"
#         msg += f"Tug'ilgan yilingiz/Date of birth - <b>{birthdate}</b> \n\n"
#         msg += f"Telefon raqamingiz/Phone Number - <b>{phone_number}</b> \n\n"
#         msg += f"Davlatlar/Countries - <b>{countries}</b> \n\n"
#         if visit_date:
#             msg += f"Tashrif sanasi/Visit Date - <b>{visit_date}</b> \n\n"
#         await message.answer(msg, reply_markup=B12UserKeyboard.confirmation)
#         await EuropeUserState.confirmation.set()
#     else:
#         await message.answer("Iltimos, to'liq ma'lumot bering! \n\nPlease, provide complete information!")

@dp.message_handler(state=EuropeUserState.visit_date, content_types=types.ContentTypes.TEXT)
async def visit(message: types, state: FSMContext):
    visit_date = message.text
    if len(visit_date) >= 3:
        await state.update_data({"visit_date": visit_date})

        await message.answer("Rasmiy ish joyingiz bormi? \n\nDo you officially work?",
                             reply_markup=B12UserKeyboard.relatives)
        await EuropeUserState.work.set()
    else:
        await message.answer("Iltimos, to'liq ma'lumot bering! \n\nPlease, provide complete information!")


@dp.message_handler(state=EuropeUserState.visit_date, content_types=types.ContentTypes.ANY)
async def visit(message: types):
    await message.answer("Iltimos, faqatgina text yozing! \n\nPlease, only write text!")

# WORK
@dp.message_handler(state=EuropeUserState.work, text="Yes/Ha")
async def work(message: types, state: FSMContext):
    await state.update_data({
        "work": "Yes"
    })
    await message.answer("Rasmiy ish joyingizni nomini kiriting \n\nWhat is the name of the company you work at?")
    await EuropeUserState.what_work.set()


@dp.message_handler(state=EuropeUserState.work, text="No/Yo'q")
async def student(message: types, state: FSMContext):
    await state.update_data({
        "work": "No"
    })
    await message.answer("Universitetda o'qiysizmi? \n\nDo you study at university?", reply_markup=B12UserKeyboard.relatives)
    await EuropeUserState.student.set()


@dp.message_handler(state=EuropeUserState.work, content_types=types.ContentTypes.ANY)
async def abroad(message: types):
    await message.answer("Iltimos, tugmalardan birini bosing! \n\nPlease, click one of the buttons",
                         reply_markup=B12UserKeyboard.relatives)


# WORKPLACE
@dp.message_handler(state=EuropeUserState.what_work, content_types=types.ContentTypes.TEXT)
async def what_work(message: types, state: FSMContext):
    workplace = str(message.text)

    if len(workplace) >= 3:
        await state.update_data({
            "workplace": workplace
        })
        await message.answer("Kim bo'lib ishlaysiz? \n\nWhat is your position at the company?")
        await EuropeUserState.work_position.set()
    else:
        await message.answer("Iltimos, to'liq ma'lumot bering! \n\nPlease, provide complete information!")


@dp.message_handler(state=EuropeUserState.what_work, content_types=types.ContentTypes.ANY)
async def work(message: types, state: FSMContext):
    await message.answer("Iltimos, faqatgina text yozing! \n\nPlease, only write text!")


# WORK POSITION
@dp.message_handler(state=EuropeUserState.work_position, content_types=types.ContentTypes.TEXT)
async def position(message: types, state: FSMContext):
    work_position = str(message.text)

    if len(work_position) >= 3:
        await state.update_data({
            "position": work_position
        })
        await message.answer("Oyligingiz qancha? \n\nHow much is your salary?")
        await EuropeUserState.work_salary.set()
    else:
        await message.answer("Iltimos, to'liq ma'lumot bering! \n\nPlease, provide complete information!")


@dp.message_handler(state=EuropeUserState.work_position, content_types=types.ContentTypes.ANY)
async def work(message: types, state: FSMContext):
    await message.answer("Iltimos, faqatgina text yozing! \n\nPlease, only write text!")


# WORK SALARY
@dp.message_handler(state=EuropeUserState.work_salary, content_types=types.ContentTypes.TEXT)
async def position(message: types, state: FSMContext):
    work_salary = str(message.text)

    if len(work_salary) >= 3:
        await state.update_data({
            "salary": work_salary
        })
        await message.answer("Universitetda o'qiysizmi? \n\nDo you study at university?",
                             reply_markup=B12UserKeyboard.relatives)
        await EuropeUserState.student.set()
    else:
        await message.answer("Iltimos, to'liq ma'lumot bering! \n\nPlease, provide complete information!")


@dp.message_handler(state=EuropeUserState.work_salary, content_types=types.ContentTypes.ANY)
async def work(message: types, state: FSMContext):
    await message.answer("Iltimos, faqatgina text yozing! \n\nPlease, only write text!")


# STUDENT
@dp.message_handler(state=EuropeUserState.student, text="Yes/Ha")
async def work(message: types, state: FSMContext):
    await state.update_data({
        "student": "Yes"
    })
    await message.answer("Qaysi universitetda o'qiysiz? \n\nWhat is the name of your university?")
    await EuropeUserState.student_university.set()


@dp.message_handler(state=EuropeUserState.student, text="No/Yo'q")
async def student(message: types, state: FSMContext):
    await state.update_data({
        "student": "No"
    })
    data = await state.get_data()
    full_name = data.get("fullname")
    birthdate = data.get("date_of_birth")
    phone_number = data.get("phone_number")
    countries = data.get("countries")
    visit_date = data.get("visit_date")
    workplace = data.get("workplace")
    position = data.get("position")
    salary = data.get("salary")
    student = data.get("student")

    msg = "Iltimos, shaxsiy ma'lumotingiz to'g'riligini tasdiqlang! \nPlease, confirm your personal info is correct! \n \n"
    msg += f"To'liq ism/Full name - <b>{full_name}</b> \n\n"
    msg += f"Tug'ilgan yilingiz/Date of birth - <b>{birthdate}</b> \n\n"
    msg += f"Telefon raqamingiz/Phone Number - <b>{phone_number}</b> \n\n"
    msg += f"Davlatlar/Countries - <b>{countries}</b> \n\n"
    if visit_date:
        msg += f"Tashrif sanasi/Visit Date - <b>{visit_date}</b> \n\n"
    if workplace:
        msg += f"Ish Joyi/Workplace - <b>{workplace}</b> \n\n"
        msg += f"Kasb/Position - <b>{position}</b> \n\n"
        msg += f"Oylik/Salary - <b>{salary}</b> \n\n"
    msg += f"Talabamisiz/Student ? - <b>{student}</b> \n\n"

    await message.answer(msg, reply_markup=B12UserKeyboard.confirmation)
    await EuropeUserState.confirmation.set()


@dp.message_handler(state=EuropeUserState.student, content_types=types.ContentTypes.ANY)
async def abroad(message: types):
    await message.answer("Iltimos, tugmalardan birini bosing! \n\nPlease, click one of the buttons",
                         reply_markup=B12UserKeyboard.relatives)


# UNIVERSITY
@dp.message_handler(state=EuropeUserState.student_university, content_types=types.ContentTypes.TEXT)
async def what_work(message: types, state: FSMContext):
    university = str(message.text)

    if len(university) >= 3:
        await state.update_data({
            "university": university
        })
        await message.answer("Qaysi sohada o'qiysiz? \n\nWhat is your major at the university?")
        await EuropeUserState.student_major.set()
    else:
        await message.answer("Iltimos, to'liq ma'lumot bering! \n\nPlease, provide complete information!")


@dp.message_handler(state=EuropeUserState.student_university, content_types=types.ContentTypes.ANY)
async def uni(message: types, state: FSMContext):
    await message.answer("Iltimos, faqatgina text yozing! \n\nPlease, only write text!")


# MAJOR
@dp.message_handler(state=EuropeUserState.student_major, content_types=types.ContentTypes.TEXT)
async def position(message: types, state: FSMContext):
    major = str(message.text)

    if len(major) >= 3:
        await state.update_data({
            "year": major
        })
        await message.answer("Nechinchi kurs talabasisiz? \n\nWhat year are you at university?", reply_markup=UserKeyboard.university)
        await EuropeUserState.student_year.set()
    else:
        await message.answer("Iltimos, to'liq ma'lumot bering! \n\nPlease, provide complete information!")


@dp.message_handler(state=EuropeUserState.student_major, content_types=types.ContentTypes.ANY)
async def work(message: types, state: FSMContext):
    await message.answer("Iltimos, faqatgina text yozing! \n\nPlease, only write text!")


# UNIVERSITY YEAR
@dp.message_handler(text="1", content_types=types.ContentTypes.TEXT, state=EuropeUserState.student_year)
@dp.message_handler(text="2", content_types=types.ContentTypes.TEXT, state=EuropeUserState.student_year)
@dp.message_handler(text="3", content_types=types.ContentTypes.TEXT, state=EuropeUserState.student_year)
@dp.message_handler(text="4", content_types=types.ContentTypes.TEXT, state=EuropeUserState.student_year)
async def university(message: types.Message, state: FSMContext):
    year = str(message.text)
    await state.update_data({"grade": f"{year} kurs/year"})

    data = await state.get_data()
    full_name = data.get("fullname")
    birthdate = data.get("date_of_birth")
    phone_number = data.get("phone_number")
    countries = data.get("countries")
    visit_date = data.get("visit_date")
    workplace = data.get("workplace")
    position = data.get("position")
    salary = data.get("salary")
    student = data.get("student")
    university = data.get("university")
    major = data.get("year")
    year = data.get("grade")


    msg = "Iltimos, shaxsiy ma'lumotingiz to'g'riligini tasdiqlang! \nPlease, confirm your personal info is correct! \n \n"
    msg += f"To'liq ism/Full name - <b>{full_name}</b> \n\n"
    msg += f"Tug'ilgan yilingiz/Date of birth - <b>{birthdate}</b> \n\n"
    msg += f"Telefon raqamingiz/Phone Number - <b>{phone_number}</b> \n\n"
    msg += f"Davlatlar/Countries - <b>{countries}</b> \n\n"
    if visit_date:
        msg += f"Tashrif sanasi/Visit Date - <b>{visit_date}</b> \n\n"
    if workplace:
        msg += f"Ish Joyi/Workplace - <b>{workplace}</b> \n\n"
        msg += f"Kasb/Position - <b>{position}</b> \n\n"
        msg += f"Oylik/Salary - <b>{salary}</b> \n\n"
    msg += f"Talabamisiz/Student ? - <b>{student}</b> \n\n"
    msg += f"Universitet/University - <b>{university}</b> \n\n"
    msg += f"Soha/Major - <b>{major}</b> \n\n"
    msg += f"Kurs/Year - <b>{year}</b> \n\n"

    await message.answer(msg, reply_markup=B12UserKeyboard.confirmation)
    await EuropeUserState.confirmation.set()


@dp.message_handler(state=EuropeUserState.student_year, content_types=types.ContentTypes.ANY)
async def abroad(message: types):
    await message.answer("Iltimos, tugmalardan birini bosing! \n\nPlease, click one of the buttons",
                         reply_markup=UserKeyboard.university)


@dp.message_handler(state=EuropeUserState.confirmation, text="Tasdiqlash/Confirm! ✅")
async def type_purpose(message: types, state: FSMContext):
    user_data = await state.get_data()
    try:
        user = await db.add_Euser(
            full_name=user_data.get("fullname"),
            date_of_birth=user_data.get("date_of_birth"),
            phone_number=user_data.get("phone_number"),
            countries=user_data.get("countries"),
            visit_date=user_data.get("visit_date"),
            works=user_data.get("work"),
            workplace=user_data.get("workplace"),
            work_position=user_data.get("position"),
            salary=user_data.get("salary"),
            student=user_data.get("student"),
            university=user_data.get("university"),
            major=user_data.get("year"),
            university_year=user_data.get("grade"),
            username=user_data.get("username"),
            telegram_id=user_data.get("telegram_id")
        )
    except asyncpg.exceptions.UniqueViolationError:
        user1 = await db.select_Euser(telegram_id=user_data.get("telegram_id"))
        await message.answer(f"User '{user1[1]}' already exists in the database!")

    count = await db.count_Eusers()
    msg = f"User '{user[1]}' has been added to Europe user's database! We now have {count} users."
    await bot.send_message(chat_id=ADMINS[0], text=msg)

    await message.answer(
        "Hamkorligingiz uchun rahmat! \nTalablarimizga to’g’ri kelsangiz, sizga yaqin orada aloqaga chiqamiz. \n\nThank you for cooperation! \nWe will reach out to you soon if you meet our requirements. 🙂",
        reply_markup=ReplyKeyboardRemove(selective=True))
    await state.finish()


@dp.message_handler(state=EuropeUserState.confirmation, text="Tahrirlash/Edit ✏️")
async def type_purpose(message: types):
    await message.answer(f"Iltimos, to'liq ism va familiyangizni kiriting! \n\nPlease, fill in your full name!")
    await UserState.fullname.set()


@dp.message_handler(state=EuropeUserState.confirmation, content_types=ContentTypes.ANY)
async def buttons(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing! \n\nPlease, click one of the buttons!", reply_markup=B12UserKeyboard.confirmation)
