from aiogram import Bot, types


async def set_default_commands(bot: Bot):
    await bot.set_my_commands(
        [
            types.BotCommand(command="start", description="Qaytadan boshlash"),
            types.BotCommand(command="add", description="Formani to'ldirish"),
            types.BotCommand(command="results", description="Natijalarni ko'rish"),
            types.BotCommand(command="help", description="Yordam olish")
        ]
    )
