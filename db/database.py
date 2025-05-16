import os
import time
import asyncpg
from typing import Optional, List
from contextlib import asynccontextmanager
from dotenv import load_dotenv 
class Database:
    pool: Optional[asyncpg.pool.Pool] = None
    last_refresh_time: float = 0
    refresh_interval: int = 3600  # seconds
    # dsn: str = os.getenv("DATABASE_URL")

    @classmethod
    async def create_pool(cls):
        load_dotenv()  # Safe to call multiple times
        dsn = os.getenv("DATABASE_URL")
        if not dsn:
            raise RuntimeError("Database url is not set")
        print(f"Connecting to DB with DSN: {dsn}") 
        cls.pool = await asyncpg.create_pool(dsn=dsn, min_size=1, max_size=5)
        cls.last_refresh_time = time.time()


    @classmethod
    async def get_pool(cls):
        if cls.pool is None:
            await cls.create_pool()
        elif time.time() - cls.last_refresh_time > cls.refresh_interval:
            await cls.refresh_pool()
        return cls.pool

    @classmethod
    async def refresh_pool(cls):
        old_pool = cls.pool
        await cls.create_pool()
        if old_pool:
            await old_pool.close()

    @classmethod
    async def close_pool(cls):
        if cls.pool:
            await cls.pool.close()
            cls.pool = None

    @classmethod
    @asynccontextmanager
    async def connection(cls):
        pool = await cls.get_pool()
        async with pool.acquire() as conn:
            yield conn

    @classmethod
    async def fetch(cls, query: str, *args):
        async with cls.connection() as conn:
            return await conn.fetch(query, *args)

    @classmethod
    async def fetchrow(cls, query: str, *args):
        async with cls.connection() as conn:
            return await conn.fetchrow(query, *args)

    @classmethod
    async def execute(cls, query: str, *args):
        async with cls.connection() as conn:
            return await conn.execute(query, *args)

    @classmethod
    async def execute_many(cls, query: str, entries: List[list]):
        async with cls.connection() as conn:
            return await conn.executemany(query, entries)

    @classmethod
    @asynccontextmanager
    async def transaction(cls):
        async with cls.connection() as conn:
            async with conn.transaction():
                yield conn

    @classmethod
    async def health_check(cls) -> bool:
        try:
            await cls.execute("SELECT 1")
            return True
        except Exception:
            return False
