import asyncio
import logging
import asyncpg
from core import settings
from aiogram import Bot, Dispatcher, types

from aiogram.filters.command import Command
from core.handlers.authorization import router as auth_router

TOKEN = settings.read_config_json("C:/input.json", "TOKEN")
data_connect = settings.read_config_json("C:/input.json", "data_connect")
dsn = f'postgresql://{data_connect["user"]}:{data_connect["password"]}@{data_connect["host"]}:{data_connect["port"]}/{data_connect["database"]}?sslmode=disable'
bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    pool = await asyncpg.create_pool(dsn = dsn,     
                                     min_size=1,        # Минимальное количество соединений
                                     max_size=10,       # Максимальное количество соединений
                                     max_queries=50000, # Максимальное количество запросов на соединение
                                     max_inactive_connection_lifetime=300,  # Время жизни неактивного соединения
                                     timeout=30,        # Таймаут подключения
                                     command_timeout=60 # Таймаут выполнения команд
                                    )

    # Передаём pool в workflow_data — он будет доступен во всех хендлерах
    dp["pool"] = pool
    # Подключаем роутер авторизации
    dp.include_router(auth_router)
    # Запускаем бота
    try:
        await dp.start_polling(bot)
    finally:
        # Корректно закрываем пул при завершении
        await pool.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())    
    