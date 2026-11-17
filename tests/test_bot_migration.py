import asyncio
import io
import itertools
import json
import os
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from aiohttp import web
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from openpyxl import load_workbook

# Force the database and Telegram identity to test values before importing the bot.
TEST_SOCKET = Path(os.environ["REALCONSULTING_TEST_PG_SOCKET"])
if not TEST_SOCKET.is_absolute() or not TEST_SOCKET.is_dir():
    raise ValueError("Set REALCONSULTING_TEST_PG_SOCKET to the isolated Postgres socket directory.")

with patch.dict(os.environ, {
    "BOT_TOKEN": "123456:fixture-token",
    "ADMINS": "101",
    "DB_HOST": str(TEST_SOCKET),
    "DB_NAME": "realconsulting_fixture",
    "DB_PASS": "fixture-only",
    "DB_USER": "fixture",
}):
    from app import bot, db, dp, main
    from states.userStates import AddVideo, DeleteStates, F1UserState, UserState


class BotMigrationTest(unittest.IsolatedAsyncioTestCase):
    fixture_user = {"id": 123456, "is_bot": True, "first_name": "Fixture", "username": "fixture_bot"}

    async def asyncSetUp(self):
        self.requests = []
        self.update_ids = itertools.count(1)
        self.waiting_updates = None
        self.reply_blocked = asyncio.Event()
        self.release_reply = asyncio.Event()
        self.hold_reply = False

        # Generated inputs simulate successive user messages outside the 100 ms throttle window.
        clock = patch("middlewares.throttling.monotonic", side_effect=itertools.count(time.monotonic() + 1, 1))
        clock.start()
        self.addCleanup(clock.stop)
        server = web.Application()
        server.router.add_post("/bot{token}/{method}", self.telegram)
        runner = web.AppRunner(server, access_log=None)
        await runner.setup()
        self.addAsyncCleanup(runner.cleanup)
        site = web.TCPSite(runner, "127.0.0.1", 0)
        await site.start()
        _, port = runner.addresses[0]
        self.addCleanup(setattr, bot, "session", bot.session)
        bot.session = AiohttpSession(api=TelegramAPIServer.from_base(f"http://127.0.0.1:{port}"))
        self.addAsyncCleanup(bot.session.close)
        self.addAsyncCleanup(self.close_db)
        dp.storage.storage.clear()

    async def close_db(self):
        if db.pool is not None:
            await db.pool.close()
            db.pool = None

    async def telegram(self, request):
        method = request.match_info["method"]
        fields = dict(await request.post())
        for name, field in fields.items():
            if isinstance(field, web.FileField):
                fields[name] = field.file.read()
        self.requests.append((method, fields))

        if method == "getMe":
            result = self.fixture_user
        elif method == "getUpdates":
            result = self.waiting_updates or []
            self.waiting_updates = None
            if not result:
                await asyncio.sleep(0.01)
        elif method in {"sendMessage", "sendVideo", "sendDocument"}:
            if self.hold_reply and int(fields["chat_id"]) == 501:
                self.hold_reply = False
                self.reply_blocked.set()
                await self.release_reply.wait()
            result = {
                "message_id": next(self.update_ids), "date": int(time.time()),
                "chat": {"id": int(fields["chat_id"]), "type": "private"},
            }
        elif method in {"setMyCommands", "deleteWebhook", "deleteMessage", "answerCallbackQuery"}:
            result = True
        else:
            raise AssertionError(f"Unexpected Telegram method {method}")
        return web.json_response({"ok": True, "result": result})

    def message(self, user_id, text=None, **content):
        sequence = next(self.update_ids)
        message = {
            "message_id": sequence, "date": int(time.time()),
            "from": {"id": user_id, "is_bot": False, "first_name": "Test", "username": "fixture_user"},
            "chat": {"id": user_id, "type": "private"},
            **content,
        }
        if text is not None:
            message["text"] = text
        return {"update_id": sequence, "message": message}

    async def dispatch_message(self, user_id, text=None, **content):
        await dp.feed_raw_update(bot, self.message(user_id, text, **content))

    async def callback(self, user_id, data):
        message = self.message(user_id, "Callback fixture").pop("message")
        await dp.feed_raw_update(bot, {
            "update_id": next(self.update_ids),
            "callback_query": {
                "id": "fixture-callback", "chat_instance": "fixture-chat",
                "from": message["from"], "message": message, "data": data,
            },
        })

    def state(self, user_id):
        return dp.fsm.get_context(bot=bot, chat_id=user_id, user_id=user_id)

    async def test_polling_drains_handler_and_preserves_pending_updates(self):
        self.waiting_updates = [self.message(501, "/start")]
        self.hold_reply = True
        polling = asyncio.create_task(main())
        try:
            await asyncio.wait_for(self.reply_blocked.wait(), timeout=6)
            await asyncio.wait_for(dp.stop_polling(), timeout=6)
            self.assertFalse(polling.done())
            self.assertFalse(db.pool.is_closing())
        finally:
            self.release_reply.set()
        await asyncio.wait_for(polling, timeout=6)
        self.assertTrue(db.pool.is_closing())
        calls = dict(self.requests)
        self.assertEqual(
            [command["command"] for command in json.loads(calls["setMyCommands"]["commands"])],
            ["start", "add", "results", "help"],
        )
        self.assertEqual(calls["deleteWebhook"]["drop_pending_updates"], "false")
        self.assertEqual(set(json.loads(calls["getUpdates"]["allowed_updates"])), {"message", "callback_query"})
        self.assertEqual(await self.state(501).get_state(), UserState.start.state)

    async def test_form_navigation_contact_and_postgres_write(self):
        await dp.emit_startup(bot=bot)
        user_id = 502
        await self.dispatch_message(user_id, "/add")
        await self.dispatch_message(user_id, sticker={
            "file_id": "fixture-sticker", "file_unique_id": "fixture-sticker-unique",
            "type": "regular", "width": 1, "height": 1, "is_animated": False, "is_video": False,
        })
        self.assertIn("only use letters", self.requests[-1][1]["text"])
        self.assertEqual(await self.state(user_id).get_state(), UserState.fullname.state)
        for text in ("Migration Test User", "January 1, 2000", "O'zbekistonda | In Uzbekistan"):
            await self.dispatch_message(user_id, text)
        await self.dispatch_message(user_id, contact={
            "phone_number": "+998901234567", "first_name": "Test", "user_id": user_id,
        })
        self.assertEqual(await self.state(user_id).get_state(), F1UserState.grade.state)
        for text in (
            "Maktabda o'qiyman | At high school", "11", "Bakalavr | Bachelor's",
            "IELTS", "7.0", "Tasdiqlash/Confirm! ✅",
        ):
            await self.dispatch_message(user_id, text)
        user = await db.select_user(telegram_id=user_id)
        self.assertEqual(user["full_name"], "Migration Test User")
        self.assertEqual(user["test_score"], "IELTS 7.0")
        self.assertIn("You meet our requirements", self.requests[-1][1]["text"])
        self.assertIsNone(await self.state(user_id).get_state())
        self.assertEqual(await self.state(user_id).get_data(), {})

    async def test_admin_video_callbacks_and_xlsx_export(self):
        await dp.emit_startup(bot=bot)
        if not await db.select_user(telegram_id=505):
            await db.add_user(
                "Export Fixture", "January 1, 2000", "+998901234567", "11 sinf",
                "bachelor's", "IELTS 7.0", "fixture_user", 505,
            )
        await self.dispatch_message(503, "/add_video")
        self.assertIn("don't qualify", self.requests[-1][1]["text"])
        await self.dispatch_message(101, "/add_video")
        self.assertEqual(await self.state(101).get_state(), AddVideo.start.state)
        await self.dispatch_message(101, document={
            "file_id": "fixture-document", "file_unique_id": "fixture-document-unique",
        })
        await self.dispatch_message(101, "Migration Video")
        await self.dispatch_message(101, "Fixture caption")
        self.assertEqual(self.requests[-2][0], "sendDocument")
        await self.dispatch_message(101, "Confirm! ✅")
        self.assertEqual((await db.select_video(keyword="Migration Video"))["caption"], "Fixture caption")

        await self.dispatch_message(101, "/delete_video")
        await self.callback(101, "Migration Video")
        self.assertEqual(await self.state(101).get_state(), DeleteStates.delete.state)
        await self.callback(101, "Migration Video")
        self.assertIsNone(await db.select_video(keyword="Migration Video"))

        await self.dispatch_message(101, "/download_data")
        method, fields = self.requests[-1]
        self.assertEqual(method, "sendDocument")
        # The multipart attachment is a real workbook, created by the unchanged export code.
        workbook_data = next(field for field in fields.values() if isinstance(field, bytes))
        workbook = load_workbook(io.BytesIO(workbook_data))
        self.assertEqual(workbook["Users"]["B1"].value, "full_name")
        workbook.close()
