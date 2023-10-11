import asyncpg
import asyncio

from config import *

"""
    def __init__(self, PGUSER, DBNAME, PGPASSWORD, IP, DBPORT):
        loop = asyncio.get_event_loop()
        self.pool: asyncpg.Pool = loop.run_until_complete(
            asyncpg.create_pool(
                user=PGUSER,
                database=DBNAME,
                password=PGPASSWORD,
                host=IP,
                port=DBPORT,
                loop=loop
            )
        )
"""

class Database:
    def __init__(self):
        loop = asyncio.get_event_loop()
        self.pool : asyncpg.Pool = loop.run_until_complete(
            asyncpg.create_pool(
                user = PGUSER,
                database = DBNAME,
                password = PGPASSWORD,
                host = IP,
                port = DBPORT,
                loop = loop
            )
        )

    async def userCreate(self, tid, name, age, description, language):
        sql = "INSERT INTO users(tid, name, age, description, language) VALUES ($1, $2, $3, $4, $5)"
        await self.pool.execute(sql, tid, name, age, description, language)

    async def isExists(self, tid):
        sql = "SELECT * FROM users WHERE tid=$1"
        query = (await self.pool.fetch(sql, tid))
        return query

    async def select_test_info(self, test_name):
        sql = "SELECT * FROM $1"
        res = (await self.pool.fetch(sql, test_name))
        return res