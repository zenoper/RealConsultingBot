import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from states.userStates import B1UserState
from keyboards.default import B12UserKeyboard
from aiogram.types import ReplyKeyboardRemove
from data.config import ADMINS


@dp.message_handler(state=B1UserState.abroad, text="Yes/Ha")
async def abroad(message: types):
    await message.answer("Iltimos, siz bo'lgan davlatlar nomini yozib qoldiring")
    await B1UserState.countries.set()


@dp.message_handler(state=B1UserState.abroad, text="No/Yo'q")
async def abroad(message: types, state: FSMContext):
    await state.update_data({"countries": "No"})
    await message.answer("Amerikada yashovchi qarindoshlaringiz bormi? \n\nDo you have relatives in the USA?",
                         reply_markup=B12UserKeyboard.relatives)
    await B1UserState.relatives.set()


@dp.message_handler(state=B1UserState.abroad, content_types=types.ContentTypes.ANY)
async def abroad(message: types):
    await message.answer("Iltimos, tugmalardan birini bosing! \n\nPlease, click one of the buttons",
                         reply_markup=B12UserKeyboard.countries)
    await B1UserState.countries.set()


@dp.message_handler(state=B1UserState.countries, content_types=types.ContentTypes.TEXT)
async def country(message: types, state: FSMContext):
    countries = message.text
    await state.update_data({"countries": countries})
    await message.answer("U yer(lar)da qachon bo'lgansiz? \nMasalan: Mart, 2021 \n\nWhen have you been there? \nFor example, March, 2021")
    await B1UserState.visit_date.set()


@dp.message_handler(state=B1UserState.countries, content_types=types.ContentTypes.ANY)
async def country(message: types):
    await message.answer("Iltimos, faqatgina text yozing! \n\nPlease, only write text!")


@dp.message_handler(state=B1UserState.visit_date, content_types=types.ContentTypes.TEXT)
async def visit(message: types, state: FSMContext):
    visit_date = message.text
    if len(visit_date) >= 3:
        await state.update_data({"visit_date": visit_date})
        await message.answer("Amerikada yashovchi qarindoshlaringiz bormi? \n\nDo you have relatives in the USA?",
                             reply_markup=B12UserKeyboard.relatives)
        await B1UserState.relatives.set()
    else:
        await message.answer("Iltimos, to'liq ma'lumot bering! \n\nPlease, provide complete information!")


@dp.message_handler(state=B1UserState.visit_date, content_types=types.ContentTypes.ANY)
async def visit(message: types):
    await message.answer("Iltimos, faqatgina text yozing! \n\nPlease, only write text!")


#RELATIVES

@dp.message_handler(state=B1UserState.relatives, text="Yes/Ha")
async def relative(message: types.Message, state: FSMContext):
    await state.update_data({"relatives": "Yes"})
    await message.answer("Qarindoshlaringiz Amerikaga qaysi visa turi orqali borishgan? \n\nWith which visa type did your relatives go to the USA?")
    await B1UserState.relative_visa.set()


@dp.message_handler(state=B1UserState.relatives, text="No/Yo'q")
async def relative(message: types.Message, state: FSMContext):
    await state.update_data({"relatives": "No"})
    await message.answer("Amerikaga borishdan maqsadingiz nima? \n\nWhat’s your purpose of visiting the USA?")
    await B1UserState.purpose.set()


@dp.message_handler(state=B1UserState.relatives, content_types=types.ContentTypes.ANY)
async def relative(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing! \n\nPlease, click one of the buttons!",
                         reply_markup=B12UserKeyboard.relatives)


@dp.message_handler(state=B1UserState.relative_visa, content_types=types.ContentTypes.TEXT)
async def type_visa(message: types.Message, state: FSMContext):
    relative_visa = message.text
    await state.update_data({"relative_visa": relative_visa})
    await message.answer("Amerikaga borishdan maqsadingiz nima? \n\nWhat’s your purpose of visiting the USA?")
    await B1UserState.purpose.set()


@dp.message_handler(state=B1UserState.relative_visa, content_types=types.ContentTypes.ANY)
async def type_visa(message: types.Message):
    await message.answer("Iltimos, faqatgina text yozing! \n\nPlease, only write text!")


#PURPOSE

@dp.message_handler(state=B1UserState.purpose, content_types=types.ContentTypes.TEXT)
async def type_purpose(message: types, state: FSMContext):
    purpose = message.text
    if len(purpose) >= 3:
        await state.update_data({"purpose": purpose})
        await message.answer("Amerikada qancha vaqt bo'lmoqchisiz? \n\nHow long do you want to be in the USA?")
        await B1UserState.how_long.set()
    else:
        await message.answer("Iltimos, to'liq ma'lumot bering! \n\nPlease, provide complete information!")


@dp.message_handler(state=B1UserState.purpose, content_types=types.ContentTypes.ANY)
async def type_purpose(message: types):
    await message.answer("Iltimos, faqatgina text yozing! \n\nPlease, only write text!")


@dp.message_handler(state=B1UserState.how_long, content_types=types.ContentTypes.TEXT)
async def type_how_long(message: types.Message, state: FSMContext):
    how_long = message.text
    if len(how_long) >= 3:
        await state.update_data({"how_long": how_long})
        await message.answer("Amerikada qaysi joylariga bormoqchisiz? \n\nWhich places do you want to visit in America?")
        await B1UserState.places_to_visit.set()
    else:
        await message.answer("Iltimos, to'liq ma'lumot bering! \n\nPlease, provide complete information!")


@dp.message_handler(state=B1UserState.how_long, content_types=types.ContentTypes.ANY)
async def type_purpose(message: types):
    await message.answer("Iltimos, faqatgina text yozing! \n\nPlease, only write text!")


@dp.message_handler(state=B1UserState.places_to_visit, content_types=types.ContentTypes.TEXT)
async def type_how_long(message: types.Message, state: FSMContext):
    places_to_visit = message.text
    if len(places_to_visit) >= 3:
        await state.update_data({"places_to_visit": places_to_visit})
        data = await state.get_data()
        full_name = data.get("fullname")
        birthdate = data.get("date_of_birth")
        countries = data.get("countries")
        visit_date = data.get("visit_date")
        relatives = data.get("relatives")
        purpose = data.get("purpose")
        how_long = data.get("how_long")
        username = data.get("username")
        telegram_id = data.get("telegram_id")





        await message.answer("Iltimos, berilgan ma'lumotlarni tasdiqlang! \n\nPlease, confirm the submitted information!")
        await B1UserState.places_to_visit.set()
    else:
        await message.answer("Iltimos, to'liq ma'lumot bering! \n\nPlease, provide complete information!")


@dp.message_handler(state=B1UserState.places_to_visit, content_types=types.ContentTypes.ANY)
async def type_purpose(message: types):
    await message.answer("Iltimos, faqatgina text yozing! \n\nPlease, only write text!")