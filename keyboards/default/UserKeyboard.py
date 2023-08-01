from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

phone_number = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="raqam jo'natish 📱", request_contact=True)
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

grade = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Maktabda o'qiyman")
        ],
        [
            KeyboardButton(text="Maktabni bitirganman")
        ],
        [
            KeyboardButton(text="Universitetda o'qiyman")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

school = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="9")
        ],
        [
            KeyboardButton(text="10")
        ],
        [
            KeyboardButton(text="11")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

university = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="1")
        ],
        [
            KeyboardButton(text="2")
        ],
        [
            KeyboardButton(text="3")
        ],
        [
            KeyboardButton(text="4")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

degree = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Bakalavr")
        ],
        [
            KeyboardButton(text="Magistratura")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

test_score = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="IELTS")
        ],
        [
            KeyboardButton(text="Duolingo")
        ],
        [
            KeyboardButton(text="None")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

confirmation = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Confirm! ✅")
        ],
        [
            KeyboardButton(text="Edit ✏️")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)



