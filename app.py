from aiogram import executor

from loader import dp, db, bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


"""
     find . -type d -name "__pycache__" -exec rm -r {} +
     find . -type f -name "*.pyc" -delete
"""


async def on_startup(dispatcher):
    await db.create()
    # await db.drop_users()
    # await db.drop_b1users()
    # await db.drop_videos()
    # await db.drop_Cusers()
    # await db.drop_Eusers()
    await db.create_table_Eusers()
    await db.create_table_users()
    await db.create_table_b1users()
    await db.create_table_videos()
    await db.create_table_Cusers()

    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)
    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
