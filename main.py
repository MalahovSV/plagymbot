import asyncio
import logging
import asyncpg
from core import settings
from aiogram import Bot, Dispatcher, types

from aiogram.filters.command import Command

TOKEN = settings.read_config_json("C:/input.json", "TOKEN")
data_connect = settings.read_config_json("C:/input.json", "data_connect")
dsn = f'postgresql://{data_connect["user"]}:{data_connect["password"]}@{data_connect["host"]}:{data_connect["port"]}/{data_connect["database"]}?sslmode=disable'

async def main():
    pool = await asyncpg.create_pool(dsn = dsn,     
                               min_size=1,        # Минимальное количество соединений
                               max_size=10,       # Максимальное количество соединений
                               max_queries=50000, # Максимальное количество запросов на соединение
                               max_inactive_connection_lifetime=300,  # Время жизни неактивного соединения
                               timeout=30,        # Таймаут подключения
                               command_timeout=60 # Таймаут выполнения команд
                               )
    user_name = "ivanov_teacher"
    password_hash = "123"
    try:
        async with pool.acquire() as conn:
            users = await conn.fetch(f"SELECT * FROM users where username = '{user_name}' and password_hash = '{password_hash}'")
    finally:
        await pool.close()
    
    print(users)
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())    
    