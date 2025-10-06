import asyncio
import asyncpg


class DatabaseManager:
    def __init__(self, data_connect):
        self.data_connect = data_connect
        self.conn = None

    async def connect(self):
        """Устанавливает соединение с БД."""
        self.conn = await asyncpg.connect(
            user=self.data_connect["user"],
            password=self.data_connect["password"],
            database=self.data_connect["database"],
            host=self.data_connect["host"],
            port=self.data_connect["port"]
        )

    async def close(self):
        if self.conn:
            await self.conn.close()
            self.conn = None

    async def execute_query_get_data(self, query, params=None):
        """Выполняет SELECT-запрос и возвращает данные."""
        if params is None:
            params = []
        return await self.conn.fetch(query, *params)

    async def execute_query(self, query, params=None):
        """Выполняет изменяющий запрос (INSERT, UPDATE, DELETE)."""
        if params is None:
            params = []
        await self.conn.execute(query, *params)

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()