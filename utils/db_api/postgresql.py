from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config

class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        date_of_birth VARCHAR(255) NOT NULL,
        phone_number VARCHAR NOT NULL,
        grade VARCHAR(255) NOT NULL,
        education_degree VARCHAR(255) NOT NULL,
        test_score VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, date_of_birth, phone_number, grade, education_degree, test_score, username, telegram_id):
        sql = "INSERT INTO Users(full_name, date_of_birth, phone_number, grade, education_degree, test_score, username, telegram_id) VALUES($1, $2, $3, $4, $5, $6, $7, $8) returning *"
        return await self.execute(sql, full_name, date_of_birth, phone_number, grade, education_degree, test_score, username, telegram_id, fetchrow=True)


    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)


    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)


    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_user(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)



#B1 or B2

    async def create_table_b1users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS B1Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        date_of_birth VARCHAR(255) NOT NULL,
        phone_number VARCHAR NOT NULL,
        countries VARCHAR(255) NOT NULL,
        visit_date VARCHAR(255) NULL,
        relatives VARCHAR(255) NOT NULL,
        relative_visa VARCHAR(255) NULL,
        purpose VARCHAR(255) NOT NULL,
        how_long VARCHAR(255) NOT NULL,
        username varchar(255) NOT NULL,
        telegram_id BIGINT NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_b1user(self, full_name, date_of_birth, phone_number, countries, visit_date, relatives, relative_visa, purpose, how_long, username, telegram_id):
        sql = "INSERT INTO B1Users(full_name, date_of_birth, phone_number, countries, visit_date, relatives, relative_visa, purpose, how_long, username, telegram_id) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11) returning *"
        return await self.execute(sql, full_name, date_of_birth, phone_number, countries, visit_date, relatives, relative_visa, purpose, how_long, username, telegram_id, fetchrow=True)

    async def select_all_b1users(self):
        sql = "SELECT * FROM B1Users"
        return await self.execute(sql, fetch=True)

    async def select_b1user(self, **kwargs):
        sql = "SELECT * FROM B1Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_b1users(self):
        sql = "SELECT COUNT(*) FROM B1Users"
        return await self.execute(sql, fetchval=True)

    async def update_b1user_username(self, username, telegram_id):
        sql = "UPDATE B1Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_b1user(self):
        await self.execute("DELETE FROM B1Users WHERE TRUE", execute=True)

    async def drop_b1users(self):
        await self.execute("DROP TABLE B1Users", execute=True)




# add video

    async def create_table_videos(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Videos (
        id SERIAL PRIMARY KEY,
        keyword VARCHAR(255) NOT NULL UNIQUE,
        file_id VARCHAR(255) NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_video(self, keyword, file_id):
        sql = "INSERT INTO Videos(keyword, file_id) VALUES($1, $2) returning *"
        return await self.execute(sql, keyword, file_id, fetchrow=True)

    async def select_all_videos(self):
        sql = "SELECT * FROM Videos"
        return await self.execute(sql, fetch=True)

    async def select_video(self, keyword):
        query = "SELECT * FROM Videos WHERE keyword = $1"
        return await self.execute(query, keyword, fetchrow=True)

    async def delete_video(self, keyword):
        query = "DELETE FROM Videos WHERE keyword = $1"
        await self.execute(query, keyword, execute=True)

    async def drop_videos(self):
        await self.execute("DROP TABLE Videos", execute=True)

