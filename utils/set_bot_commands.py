from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Qaytadan boshlash"),
            types.BotCommand("add", "Formani to'ldirish"),
            types.BotCommand("results", "Natijalarni ko'rish"),
            types.BotCommand("help", "Yordam olish")
        ]
    )
