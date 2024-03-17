import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from states.userStates import CanadaUserState, UserState
from keyboards.default import B12UserKeyboard
from aiogram.types import ReplyKeyboardRemove, ContentTypes
from data.config import ADMINS


@dp.message_handler(state=CanadaUserState.abroad, text="Yes/Ha")
async def abroad(message: types):
    await message.answer("Iltimos, siz bo'lgan davlatlar nomini yozib qoldiring")
    await CanadaUserState.countries.set()


@dp.message_handler(state=CanadaUserState.abroad, text="No/Yo'q")
async def abroad(message: types, state: FSMContext):
    await state.update_data({"countries": "No"})
    data = await state.get_data()
    full_name = data.get("fullname")
    birthdate = data.get("date_of_birth")
    phone_number = data.get("phone_number")
    countries = data.get("countries")

    msg = "Iltimos, shaxsiy ma'lumotingiz to'g'riligini tasdiqlang! \nPlease, confirm your personal info is correct! \n \n"
    msg += f"To'liq ism/Full name - <b>{full_name}</b> \n\n"
    msg += f"Tug'ilgan yilingiz/Date of birth - <b>{birthdate}</b> \n\n"
    msg += f"Telefon raqamingiz/Phone Number - <b>{phone_number}</b> \n\n"
    msg += f"Davlatlar/Countries - <b>{countries}</b> \n\n"
    await message.answer(msg, reply_markup=B12UserKeyboard.confirmation)
    await CanadaUserState.confirmation.set()


@dp.message_handler(state=CanadaUserState.abroad, content_types=ContentTypes.ANY)
async def abroad(message: types):
    await message.answer("Iltimos, tugmalardan birini bosing! \n\nPlease, click one of the buttons",
                         reply_markup=B12UserKeyboard.abroad)


@dp.message_handler(state=CanadaUserState.countries, content_types=ContentTypes.TEXT)
async def country(message: types, state: FSMContext):
    countries = message.text
    await state.update_data({"countries": countries})
    await message.answer("U davlat(lar)da qachon bo'lgansiz? \nMasalan: Mart, 2021 \n\nWhen have you been there? \nFor example, March, 2021")
    await CanadaUserState.visit_date.set()


@dp.message_handler(state=CanadaUserState.countries, content_types=types.ContentTypes.ANY)
async def country(message: types):
    await message.answer("Iltimos, faqatgina text yozing! \n\nPlease, only write text!")


@dp.message_handler(state=CanadaUserState.visit_date, content_types=types.ContentTypes.TEXT)
async def visit(message: types, state: FSMContext):
    visit_date = message.text
    if len(visit_date) >= 3:
        await state.update_data({"visit_date": visit_date})

        data = await state.get_data()
        full_name = data.get("fullname")
        birthdate = data.get("date_of_birth")
        phone_number = data.get("phone_number")
        countries = data.get("countries")
        visit_date = data.get("visit_date")

        msg = "Iltimos, shaxsiy ma'lumotingiz to'g'riligini tasdiqlang! \nPlease, confirm your personal info is correct! \n \n"
        msg += f"To'liq ism/Full name - <b>{full_name}</b> \n\n"
        msg += f"Tug'ilgan yilingiz/Date of birth - <b>{birthdate}</b> \n\n"
        msg += f"Telefon raqamingiz/Phone Number - <b>{phone_number}</b> \n\n"
        msg += f"Davlatlar/Countries - <b>{countries}</b> \n\n"
        if visit_date:
            msg += f"Tashrif sanasi/Visit Date - <b>{visit_date}</b> \n\n"
        await message.answer(msg, reply_markup=B12UserKeyboard.confirmation)
        await CanadaUserState.confirmation.set()
    else:
        await message.answer("Iltimos, to'liq ma'lumot bering! \n\nPlease, provide complete information!")


@dp.message_handler(state=CanadaUserState.visit_date, content_types=types.ContentTypes.ANY)
async def visit(message: types):
    await message.answer("Iltimos, faqatgina text yozing! \n\nPlease, only write text!")


@dp.message_handler(state=CanadaUserState.confirmation, text="Tasdiqlash/Confirm! ✅")
async def type_purpose(message: types, state: FSMContext):
    user_data = await state.get_data()
    try:
        user = await db.add_Cuser(
            full_name=user_data.get("fullname"),
            date_of_birth=user_data.get("date_of_birth"),
            phone_number=user_data.get("phone_number"),
            countries=user_data.get("countries"),
            visit_date=user_data.get("visit_date"),
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
    await state.finish()


@dp.message_handler(state=CanadaUserState.confirmation, text="Tahrirlash/Edit ✏️")
async def type_purpose(message: types):
    await message.answer(f"Iltimos, to'liq ism va familiyangizni kiriting! \n\nPlease, fill in your full name!")
    await UserState.fullname.set()


@dp.message_handler(state=CanadaUserState.confirmation, content_types=ContentTypes.ANY)
async def buttons(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing! \n\nPlease, click one of the buttons!", reply_markup=B12UserKeyboard.confirmation)
