import asyncio

from utils.db_api.postgresql import Database


async def test():
    db = Database()
    await db.create()

    print("Users jadvalini yaratamiz...")
    await db.drop_users()
    await db.create_table_users()
    print("Yaratildi")

    print("Foydalanuvchilarni qo'shamiz")

    await db.add_user("anvar", "April 25, 2005", "+998990083203", "maktab-9", "bakalavr", "IELTS 7", "@balobattar", 435464564564565)
    await db.add_user("MK", "OPPOSITE", "+998990083203", "Uni 2", "Magistr", "Duolingo", "@balobattarrr", 4354645564565)

    print("Qo'shildi")

    users = await db.select_all_users()
    print(f"Barcha foydalanuvchilar: {users}")

    user = await db.select_user(id=2)
    print(f"Foydalanuvchi: {user}")


asyncio.run(test())