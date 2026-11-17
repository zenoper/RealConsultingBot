import logging

from aiogram.exceptions import TelegramAPIError
from aiogram.types import ErrorEvent

from loader import dp


@dp.error()
async def errors_handler(event: ErrorEvent):
    if not isinstance(event.exception, TelegramAPIError):
        raise event.exception
    logging.error(
        "Telegram API error in update %s: %s",
        event.update.update_id,
        type(event.exception).__name__,
    )
    return True
