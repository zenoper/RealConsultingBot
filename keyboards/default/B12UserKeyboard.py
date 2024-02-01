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


relatives = ReplyKeyboardMarkup(
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


confirmation = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Tasdiqlash/Confirm! ✅")
        ],
        [
            KeyboardButton(text="Tahrirlash/Edit ✏️")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)