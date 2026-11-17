import asyncio

from aiogram import Bot

from loader import dp, db, bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


"""
     find . -type d -name "__pycache__" -exec rm -r {} +
     find . -type f -name "*.pyc" -delete
"""


async def on_startup(bot: Bot):
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
    await set_default_commands(bot)
    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(bot)
    await bot.delete_webhook(drop_pending_updates=False)


dp.startup.register(on_startup)


async def main():
    async with bot.context():
        try:
            await dp.start_polling(bot, polling_timeout=20, close_bot_session=False)
        finally:
            # aiogram 3.31 stops polling without waiting for dispatched handlers.
            # Let them finish while the Telegram session and database are open.
            await asyncio.gather(*dp._handle_update_tasks, return_exceptions=True)
            if db.pool is not None:
                await db.pool.close()


if __name__ == '__main__':
    asyncio.run(main())
