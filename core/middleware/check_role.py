from aiogram import BaseMiddleware
from asyncpg import Pool
from typing import Any, Callable, Dict, Awaitable
from aiogram.types import Message


class QualifierRole(BaseMiddleware):
    def __init__(self, pool: Pool):
        self.pool = pool
        super().__init__()
        print("Инциализация")

    async def __call__( self,
                        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                        event: Message,
                        data: Dict[str, Any]
                        ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)
        
        print("Вызван идентификатор роли")
        #user_id = event.from_user.id

        if event.text and event.text.startswith("/start"):
            print("Команда старт")
            async with self.pool.acquire() as conn:
                print("Запрос и роли")
                role = await conn.fetchval(
                    "SELECT role_id FROM users WHERE telegram_id = $1", event.from_user.id 
                )
            if role is None:
                await event.answer("Не присвоена роль. Обратитесь к администратору.")
                return
            
            data["user_role"] = role
            print("Роль пользователя: ", data["user_role"])

            return await handler(event, data)
