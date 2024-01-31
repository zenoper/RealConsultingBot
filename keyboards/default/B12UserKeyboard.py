from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


countries = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Yes/Ha")
        ],
        [
            KeyboardButton(text="No/Yo'q")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)