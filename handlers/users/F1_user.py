import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from states.userStates import UserState, GradeStates, TestStates
from keyboards.default import UserKeyboard
from aiogram.types import ReplyKeyboardRemove
from data.config import ADMINS


@dp.message_handler(text="Maktabda o'qiyman | At high school", content_types=types.ContentTypes.TEXT, state=UserState.grade)
async def school(message: types.Message):
    await message.answer("Nechinchi sinfda o'qiysiz? \n\nWhat grade at high school are you in?", reply_markup=UserKeyboard.school)
    await GradeStates.school.set()

@dp.message_handler(text="9", content_types=types.ContentTypes.TEXT, state=GradeStates.school)
@dp.message_handler(text="10", content_types=types.ContentTypes.TEXT, state=GradeStates.school)
@dp.message_handler(text="11", content_types=types.ContentTypes.TEXT, state=GradeStates.school)
async def school(message: types.Message, state: FSMContext):
    grade = message.text
    if grade == "11":
        qu_score = await state.get_data()
        q_score = qu_score.get("qualification")
        q_score += 1
        await state.update_data({"qualification": q_score})
    await state.update_data({'grade': f"{grade} sinf"})
    await message.answer("Qaysi darajada o'qimoqchisiz? Tanlang: \n\nWhat degree do you want to study at? Choose one:", reply_markup=UserKeyboard.degree)
    await UserState.degree.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=GradeStates.school)
async def school(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing! \nPlease, click one of the buttons!", reply_markup=UserKeyboard.school)


@dp.message_handler(text="Maktabni bitirganman | In a gap year", content_types=types.ContentTypes.TEXT, state=UserState.grade)
async def school(message: types.Message, state: FSMContext):
    qu_score = await state.get_data()
    q_score = qu_score.get("qualification")
    q_score += 1
    await state.update_data({"qualification": q_score})
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
    qu_score = await state.get_data()
    q_score = qu_score.get("qualification")
    q_score += 1
    await state.update_data({"qualification": q_score})
    await state.update_data({"grade": f"{year} kurs/year"})
    await message.answer("Qaysi darajada o'qimoqchisiz? Tanlang: \n\nWhat degree do you want to study at? Choose one:", reply_markup=UserKeyboard.degree)
    await UserState.degree.set()

@dp.message_handler(content_types=types.ContentTypes.ANY, state=GradeStates.university)
async def school(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing! \nPlease, click one of the buttons!", reply_markup=UserKeyboard.university)


@dp.message_handler(text="Universitetni bitirganman | Graduated university", content_types=types.ContentTypes.TEXT,state=UserState.grade)
async def university(message: types.Message, state: FSMContext):
    qu_score = await state.get_data()
    q_score = qu_score.get("qualification")
    q_score += 1
    await state.update_data({"qualification": q_score})
    await state.update_data({"grade": "graduated university"})
    await message.answer("Qaysi darajada o'qimoqchisiz? Tanlang: \n\nWhat degree do you want to study at? Choose one:", reply_markup=UserKeyboard.degree)
    await UserState.degree.set()

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

            if degree_of == "bachelor's" and float(ielts_of) >= 5.5:
                qu_score = await state.get_data()
                q_score = qu_score.get("qualification")
                q_score += 1
                await state.update_data({"qualification": q_score})

            if degree_of == "master's" and float(ielts_of) >= 6:
                qu_score = await state.get_data()
                q_score = qu_score.get("qualification")
                q_score += 1
                await state.update_data({"qualification": q_score})

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

        if degree_of == "bachelor's" and float(duolingo_of) >= 100:
            qu_score = await state.get_data()
            q_score = qu_score.get("qualification")
            q_score += 1
            await state.update_data({"qualification": q_score})

        if degree_of == "master's" and float(duolingo_of) >= 105:
            qu_score = await state.get_data()
            q_score = qu_score.get("qualification")
            q_score += 1
            await state.update_data({"qualification": q_score})

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

    intended_degree = user_data.get("degree")
    current_degree = user_data.get("grade")
    if intended_degree == "bachelor's" and current_degree == "11 sinf":
        q_score = user_data.get("qualification")
        q_score += 1
        await state.update_data({"qualification": q_score})
    elif intended_degree == "bachelor's" and current_degree == "maktabni bitirgan/gap year":
        q_score = user_data.get("qualification")
        q_score += 1
        await state.update_data({"qualification": q_score})
    elif intended_degree == "bachelor's" and current_degree == "graduated university":
        q_score = user_data.get("qualification")
        q_score += 1
        await state.update_data({"qualification": q_score})
    if intended_degree == "bachelor's" and current_degree == "1 kurs/year":
        q_score = user_data.get("qualification")
        q_score += 1
        await state.update_data({"qualification": q_score})
    elif intended_degree == "bachelor's" and current_degree == "2 kurs/year":
        q_score = user_data.get("qualification")
        q_score += 1
        await state.update_data({"qualification": q_score})
    elif intended_degree == "bachelor's" and current_degree == "3 kurs/year":
        q_score = user_data.get("qualification")
        q_score += 1
        await state.update_data({"qualification": q_score})
    elif intended_degree == "bachelor's" and current_degree == "4 kurs/year":
        q_score = user_data.get("qualification")
        q_score += 1
        await state.update_data({"qualification": q_score})
    if intended_degree == "master's" and current_degree == "4 kurs/year":
        q_score = user_data.get("qualification")
        q_score += 1
        await state.update_data({"qualification": q_score})
    elif intended_degree == "master's" and current_degree == "graduated university":
        q_score = user_data.get("qualification")
        q_score += 1
        await state.update_data({"qualification": q_score})

    qu_score = await state.get_data()
    qualification_score = qu_score.get("qualification")
    if qualification_score >= 3:
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

        await message.answer("Hamkorligingiz uchun rahmat! \nBizni talablarimizga to'g'ri keldingiz ✅. Sizga yaqin orada aloqaga chiqamiz. \n\nThank you for cooperation! \nYou meet our requirements ✅. We will reach out to you soon. 🙂", reply_markup=ReplyKeyboardRemove(selective=True))
        await state.finish()
    else:
        user_data = await state.get_data()
        q_scoree = user_data.get("qualification")
        await message.answer(
            "Hamkorligingiz uchun rahmat! \nUzr, bizni talablarimizga to'g'ri kelmadingiz ❌. Test natijalaringiz yetarli darajada emas, yoki o'quv yilingiz va maqsadlaringiz bizning talablarimizga mos tushmaydi. \n\nThank you for cooperation! Sorry, but you don't meet our requirements ❌. Either you have a low test score or your current education level and educational goals don't suit.",
            reply_markup=ReplyKeyboardRemove(selective=True))
        await message.answer(" Talablar: \n\n🎓 Bakalavrga hozirda 11-sinfda o’qiyotgan yoki maktabni bitirgan bo'lishingiz kerak. \nIELTS 5.5 or above \nDuolingo 100 or above \n\n‍🎓 Magistratura uchun esa hozirda bakalavrda 4-kursda o’qiyotgan yoki allaqachon universitetni bitirgan bo’lishingiz zarur. \nIELTS 6 or above \nDuolingo 105 or above ")
        await state.finish()


@dp.message_handler(text="Tahrirlash/Edit ✏️", content_types=types.ContentTypes.TEXT, state=UserState.confirmation)
async def edit(message: types.Message):
    await message.answer("Iltimos, to'liq ismingizni kiriting! \n\nPlease, fill in your full name!")
    await UserState.fullname.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=UserState.confirmation)
async def confirmation(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing! \nPlease, click one of the buttons!", reply_markup=UserKeyboard.confirmation)

