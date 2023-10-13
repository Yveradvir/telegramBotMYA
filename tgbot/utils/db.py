import asyncpg
from config import *

class Database:
    def __init__(self):
        self.conn: asyncpg.Connection = None

    async def __aenter__(self):
        self.conn = await asyncpg.connect(
            database=DBNAME,
            user=PGUSER,
            password=PGPASSWORD,
            host=IP,
            port=DBPORT
        )
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.conn.close()

    async def userCreate(self, tid, name, age, description, language, exist):
        if exist: sql = "UPDATE users SET name=$2, age=$3, description=$4, language=$5 WHERE tid=$1"
        else:     sql = "INSERT INTO users(tid, name, age, description, language) VALUES ($1, $2, $3, $4, $5)"
        await self.conn.execute(sql, tid, name, age, description, language)

    async def userDelete(self, tid):
        sql = "DELETE FROM users WHERE tid=$1"
        await self.conn.execute(sql, tid)

    async def isExists(self, tid):
        sql = "SELECT * FROM users WHERE tid=$1"
        query = await self.conn.fetch(sql, tid)
        return query
