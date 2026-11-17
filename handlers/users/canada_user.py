import asyncpg.exceptions
from aiogram import F, types
from aiogram.filters import StateFilter
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from loader import dp, db, bot
from states.userStates import CanadaUserState, UserState
from keyboards.default import B12UserKeyboard, UserKeyboard
from aiogram.types import ReplyKeyboardRemove
from data.config import ADMINS


@dp.message(StateFilter(CanadaUserState.abroad), F.text == 'Yes/Ha')
async def abroad(message: types, state: FSMContext):
    await message.answer("Iltimos, siz bo'lgan davlatlar nomini yozib qoldiring")
    await state.set_state(CanadaUserState.countries)


@dp.message(StateFilter(CanadaUserState.abroad), F.text == "No/Yo'q")
async def abroad(message: types, state: FSMContext):
    await state.update_data({"countries": "No"})
    await message.answer("Rasmiy ish joyingiz bormi? \n\nDo you officially work?", reply_markup=B12UserKeyboard.relatives)
    await state.set_state(CanadaUserState.work)


@dp.message(StateFilter(CanadaUserState.abroad))
async def abroad(message: types):
    await message.answer("Iltimos, tugmalardan birini bosing! \n\nPlease, click one of the buttons",
                         reply_markup=B12UserKeyboard.abroad)


@dp.message(StateFilter(CanadaUserState.countries), F.content_type == ContentType.TEXT)
async def country(message: types, state: FSMContext):
    countries = message.text
    await state.update_data({"countries": countries})
    await message.answer("U davlat(lar)da qachon bo'lgansiz? \nMasalan: Mart, 2021 \n\nWhen have you been there? \nFor example, March, 2021")
    await state.set_state(CanadaUserState.visit_date)


@dp.message(StateFilter(CanadaUserState.countries))
async def country(message: types):
    await message.answer("Iltimos, faqatgina text yozing! \n\nPlease, only write text!")


# @dp.message_handler(state=CanadaUserState.visit_date, content_types=types.ContentTypes.TEXT)
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
#         await CanadaUserState.confirmation.set()
#     else:
#         await message.answer("Iltimos, to'liq ma'lumot bering! \n\nPlease, provide complete information!")

@dp.message(StateFilter(CanadaUserState.visit_date), F.content_type == ContentType.TEXT)
async def visit(message: types, state: FSMContext):
    visit_date = message.text
    if len(visit_date) >= 3:
        await state.update_data({"visit_date": visit_date})

        await message.answer("Rasmiy ish joyingiz bormi? \n\nDo you officially work?",
                             reply_markup=B12UserKeyboard.relatives)
        await state.set_state(CanadaUserState.work)
    else:
        await message.answer("Iltimos, to'liq ma'lumot bering! \n\nPlease, provide complete information!")


@dp.message(StateFilter(CanadaUserState.visit_date))
async def visit(message: types):
    await message.answer("Iltimos, faqatgina text yozing! \n\nPlease, only write text!")

# WORK
@dp.message(StateFilter(CanadaUserState.work), F.text == 'Yes/Ha')
async def work(message: types, state: FSMContext):
    await state.update_data({
        "work": "Yes"
    })
    await message.answer("Rasmiy ish joyingizni nomini kiriting \n\nWhat is the name of the company you work at?")
    await state.set_state(CanadaUserState.what_work)


@dp.message(StateFilter(CanadaUserState.work), F.text == "No/Yo'q")
async def student(message: types, state: FSMContext):
    await state.update_data({
        "work": "No"
    })
    await message.answer("Universitetda o'qiysizmi? \n\nDo you study at university?", reply_markup=B12UserKeyboard.relatives)
    await state.set_state(CanadaUserState.student)


@dp.message(StateFilter(CanadaUserState.work))
async def abroad(message: types):
    await message.answer("Iltimos, tugmalardan birini bosing! \n\nPlease, click one of the buttons",
                         reply_markup=B12UserKeyboard.relatives)


# WORKPLACE
@dp.message(StateFilter(CanadaUserState.what_work), F.content_type == ContentType.TEXT)
async def what_work(message: types, state: FSMContext):
    workplace = str(message.text)

    if len(workplace) >= 3:
        await state.update_data({
            "workplace": workplace
        })
        await message.answer("Kim bo'lib ishlaysiz? \n\nWhat is your position at the company?")
        await state.set_state(CanadaUserState.work_position)
    else:
        await message.answer("Iltimos, to'liq ma'lumot bering! \n\nPlease, provide complete information!")


@dp.message(StateFilter(CanadaUserState.what_work))
async def work(message: types, state: FSMContext):
    await message.answer("Iltimos, faqatgina text yozing! \n\nPlease, only write text!")


# WORK POSITION
@dp.message(StateFilter(CanadaUserState.work_position), F.content_type == ContentType.TEXT)
async def position(message: types, state: FSMContext):
    work_position = str(message.text)

    if len(work_position) >= 3:
        await state.update_data({
            "position": work_position
        })
        await message.answer("Oyligingiz qancha? \n\nHow much is your salary?")
        await state.set_state(CanadaUserState.work_salary)
    else:
        await message.answer("Iltimos, to'liq ma'lumot bering! \n\nPlease, provide complete information!")


@dp.message(StateFilter(CanadaUserState.work_position))
async def work(message: types, state: FSMContext):
    await message.answer("Iltimos, faqatgina text yozing! \n\nPlease, only write text!")


# WORK SALARY
@dp.message(StateFilter(CanadaUserState.work_salary), F.content_type == ContentType.TEXT)
async def position(message: types, state: FSMContext):
    work_salary = str(message.text)

    if len(work_salary) >= 3:
        await state.update_data({
            "salary": work_salary
        })
        await message.answer("Universitetda o'qiysizmi? \n\nDo you study at university?",
                             reply_markup=B12UserKeyboard.relatives)
        await state.set_state(CanadaUserState.student)
    else:
        await message.answer("Iltimos, to'liq ma'lumot bering! \n\nPlease, provide complete information!")


@dp.message(StateFilter(CanadaUserState.work_salary))
async def work(message: types, state: FSMContext):
    await message.answer("Iltimos, faqatgina text yozing! \n\nPlease, only write text!")


# STUDENT
@dp.message(StateFilter(CanadaUserState.student), F.text == 'Yes/Ha')
async def work(message: types, state: FSMContext):
    await state.update_data({
        "student": "Yes"
    })
    await message.answer("Qaysi universitetda o'qiysiz? \n\nWhat is the name of your university?")
    await state.set_state(CanadaUserState.student_university)


@dp.message(StateFilter(CanadaUserState.student), F.text == "No/Yo'q")
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
    work = data.get("work")
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
    await state.set_state(CanadaUserState.confirmation)


@dp.message(StateFilter(CanadaUserState.student))
async def abroad(message: types):
    await message.answer("Iltimos, tugmalardan birini bosing! \n\nPlease, click one of the buttons",
                         reply_markup=B12UserKeyboard.relatives)


# UNIVERSITY
@dp.message(StateFilter(CanadaUserState.student_university), F.content_type == ContentType.TEXT)
async def what_work(message: types, state: FSMContext):
    university = str(message.text)

    if len(university) >= 3:
        await state.update_data({
            "university": university
        })
        await message.answer("Qaysi sohada o'qiysiz? \n\nWhat is your major at the university?")
        await state.set_state(CanadaUserState.student_major)
    else:
        await message.answer("Iltimos, to'liq ma'lumot bering! \n\nPlease, provide complete information!")


@dp.message(StateFilter(CanadaUserState.student_university))
async def uni(message: types, state: FSMContext):
    await message.answer("Iltimos, faqatgina text yozing! \n\nPlease, only write text!")


# MAJOR
@dp.message(StateFilter(CanadaUserState.student_major), F.content_type == ContentType.TEXT)
async def position(message: types, state: FSMContext):
    major = str(message.text)

    if len(major) >= 3:
        await state.update_data({
            "year": major
        })
        await message.answer("Nechinchi kurs talabasisiz? \n\nWhat year are you at university?", reply_markup=UserKeyboard.university)
        await state.set_state(CanadaUserState.student_year)
    else:
        await message.answer("Iltimos, to'liq ma'lumot bering! \n\nPlease, provide complete information!")


@dp.message(StateFilter(CanadaUserState.student_major))
async def work(message: types, state: FSMContext):
    await message.answer("Iltimos, faqatgina text yozing! \n\nPlease, only write text!")


# UNIVERSITY YEAR
@dp.message(StateFilter(CanadaUserState.student_year), F.text == '1')
@dp.message(StateFilter(CanadaUserState.student_year), F.text == '2')
@dp.message(StateFilter(CanadaUserState.student_year), F.text == '3')
@dp.message(StateFilter(CanadaUserState.student_year), F.text == '4')
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
    await state.set_state(CanadaUserState.confirmation)


@dp.message(StateFilter(CanadaUserState.student_year))
async def abroad(message: types):
    await message.answer("Iltimos, tugmalardan birini bosing! \n\nPlease, click one of the buttons",
                         reply_markup=UserKeyboard.university)


@dp.message(StateFilter(CanadaUserState.confirmation), F.text == 'Tasdiqlash/Confirm! ✅')
async def type_purpose(message: types, state: FSMContext):
    user_data = await state.get_data()
    try:
        user = await db.add_Cuser(
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
        user1 = await db.select_Cuser(telegram_id=user_data.get("telegram_id"))
        await message.answer(f"User '{user1[1]}' already exists in the database!")

    count = await db.count_Cusers()
    msg = f"User '{user[1]}' has been added to Canada user's database! We now have {count} users."
    await bot.send_message(chat_id=ADMINS[0], text=msg)

    await message.answer(
        "Hamkorligingiz uchun rahmat! \nTalablarimizga to’g’ri kelsangiz, sizga yaqin orada aloqaga chiqamiz. \n\nThank you for cooperation! \nWe will reach out to you soon if you meet our requirements. 🙂",
        reply_markup=ReplyKeyboardRemove(selective=True))
    await state.clear()


@dp.message(StateFilter(CanadaUserState.confirmation), F.text == 'Tahrirlash/Edit ✏️')
async def type_purpose(message: types, state: FSMContext):
    await message.answer(f"Iltimos, to'liq ism va familiyangizni kiriting! \n\nPlease, fill in your full name!")
    await state.set_state(UserState.fullname)


@dp.message(StateFilter(CanadaUserState.confirmation))
async def buttons(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing! \n\nPlease, click one of the buttons!", reply_markup=B12UserKeyboard.confirmation)
