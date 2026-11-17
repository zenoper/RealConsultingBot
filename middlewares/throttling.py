from time import monotonic

from aiogram import BaseMiddleware
from aiogram.types import Message


class ThrottlingMiddleware(BaseMiddleware):
    """Rate limit each message handler per chat and sender."""

    def __init__(self, limit=0.1, key_prefix="antiflood_"):
        self.rate_limit = limit
        self.prefix = key_prefix
        self.calls = {}
        self.next_cleanup = monotonic() + 60

    async def __call__(self, handler, message: Message, data: dict):
        callback = data["handler"].callback
        limit = getattr(callback, "throttling_rate_limit", self.rate_limit)
        key = getattr(callback, "throttling_key", f"{self.prefix}_{callback.__name__}")
        sender_id = message.from_user.id if message.from_user else None
        bucket = (message.chat.id, sender_id, key)
        now = monotonic()
        if now >= self.next_cleanup:
            self.calls = {key: call for key, call in self.calls.items() if call[2] > now}
            self.next_cleanup = now + 60

        previous, count, _ = self.calls.get(bucket, (now, 0, now))
        if previous < now < previous + limit:
            self.calls[bucket] = (now, count + 1, now + limit)
            if count == 1:
                await message.reply("Too many requests!")
            return None
        self.calls[bucket] = (now, 1, now + limit)
        return await handler(message, data)
