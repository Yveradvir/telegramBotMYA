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


    async def userCreate(self, tid, name, age, description, language, profile, exist):
        if exist: sql = "UPDATE users SET name=$2, age=$3, description=$4, language=$5 profile=$6 WHERE tid=$1"
        else:     sql = "INSERT INTO users(tid, name, age, description, language, profile) VALUES ($1, $2, $3, $4, $5, $6)"
        await self.conn.execute(sql, tid, name, age, description, language, profile)

    async def userDelete(self, tid):
        sql = "DELETE FROM users WHERE tid=$1"
        await self.conn.execute(sql, tid)

    async def isExists(self, tid, byId=False):
        if byId: sql = "SELECT * FROM users WHERE id=$1"
        else: sql = "SELECT * FROM users WHERE tid=$1"
        query = await self.conn.fetch(sql, tid)
        return query

    async def getFromUser(self, what, tid):
        sql = "SELECT $1 FROM users WHERE tid=$2"
        return await self.conn.fetch(sql, what, tid)
    
    async def allTableCount(self, table):
        sql = f"SELECT COUNT(*) FROM {table}"
        print(await self.conn.fetchval(sql))
        return await self.conn.fetchval(sql)
    #--post

    async def postCreate(self, title, content, aid, uid):
        sql = "INSERT INTO posts(title, content, answer_id, author_id) VALUES $1, $2, $3, $4"
        await self.conn.execute(sql, title, content, aid, uid)

    async def isExistsPost(self, postId):
        sql = "SELECT * FROM posts WHERE id = ?"
        return await self.conn.fetch(sql, postId)