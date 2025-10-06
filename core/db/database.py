# database.py
import asyncpg
from typing import Optional

class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def create_pool(self, dsn: str):
        self.pool = await asyncpg.create_pool(dsn=dsn)

    async def close_pool(self):
        if self.pool:
            await self.pool.close()

    # Пример метода для получения пользователя
    async def get_user(self, user_id: int):
        return await self.pool.fetchrow(
            f"SELECT get_user_id_by_telegram_id({user_id})",
            user_id
        )

    # Пример метода для добавления пользователя
    async def add_user(self, user_id: int, username: str, full_name: str):
        await self.pool.execute(
            """
            INSERT INTO users (telegram_id, username, full_name)
            VALUES ($1, $2, $3)
            ON CONFLICT (telegram_id) DO NOTHING
            """,
            user_id, username, full_name
        )