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

degree = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Maktabda")
        ],
        [
            KeyboardButton(text="Universitetda")
        ],
        [
            KeyboardButton(text="Bitirganman")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)