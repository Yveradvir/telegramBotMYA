import asyncio, asyncpg

from config import *
from config import PGUSER, DBNAME, PGPASSWORD, IP, DBPORT

class Database:
    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.pool : asyncpg.Pool = self.loop.run_until_complete(
            asyncpg.create_pool(
                user=PGUSER,
                database=DBNAME,
                password=PGPASSWORD,
                host=IP,
                port=DBPORT,
                loop=self.loop
            )
        )

    async def reg(self, id, nickname, age, city):
        exists = await self.hook_exists(id)


        sql = "INSERT INTO users(id, nickname, age, city) VALUES ($1, $2, $3, $4)" \
        if not exists else "UPDATE users SET name = $1, age = $2, city = $3 WHERE id = $4"
        
        await self.pool.execute(sql, id, nickname, age, city)

    async def hook_exists(self, id):
        sql = "SELECT COUNT(*) FROM users WHERE id = $1;"
        hook = await self.pool.fetchval(sql, id)
        
        return hook > 0

    async def deactivation(self, id):
        exists = await self.hook_exists(id)

        if exists:
            try:
                sql = "DELETE FROM posts WHERE author_id = $1"
                await self.pool.execute(sql, id)
            except Exception as e:
                print(e)
            finally:    
                sql = "DELETE FROM users WHERE id = $1"
                await self.pool.execute(sql, id)
            
            return "I am delete your account"
        else:
            return "Sorry, but you not register"
    
    async def post(self, id, title, content, oldMark, tag):
        sql = "INSERT INTO posts(title, content, oldMark, tag, author_id) VALUES ($1, $2, $3, $4, $5)"
        await self.pool.execute(sql, title, content, oldMark, tag, id)
    
    async def return_all_my_post(self, id):
        sql = "SELECT id, title FROM posts WHERE author_id = $1"
        return await self.pool.fetch(sql, id)
    