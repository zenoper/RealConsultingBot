from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

intorlocal = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="O'zbekistonda | In Uzbekistan")
        ],
        [
            KeyboardButton(text="Chet-elda | Abroad")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

phone_number = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="raqam jo'natish | send phone number 📱", request_contact=True)
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

grade = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Maktabda o'qiyman | At high school")
        ],
        [
            KeyboardButton(text="Maktabni bitirganman | In a gap year")
        ],
        [
            KeyboardButton(text="Universitetda o'qiyman | At university")
        ],
        [
            KeyboardButton(text="Universitetni bitirganman | Graduated university")
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
            KeyboardButton(text="1"),
            KeyboardButton(text="2")
        ],
        [
            KeyboardButton(text="3"),
            KeyboardButton(text="4")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

degree = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Bakalavr | Bachelor's")
        ],
        [
            KeyboardButton(text="Magistratura | Master's")
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
            KeyboardButton(text="Yo'q/None")
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



