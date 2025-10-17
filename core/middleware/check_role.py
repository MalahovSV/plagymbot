from aiogram import BaseMiddleware
from asyncpg import Pool
from typing import Any, Callable, Dict, Awaitable
from aiogram.types import Message
from core.utils.StateReporter import StateReporterMiddleware


consoleLogger = StateReporterMiddleware("check_role")
class QualifierRole(BaseMiddleware):
    def __init__(self, pool: Pool):
        self.pool = pool
        super().__init__()
        

    async def __call__( self,
                        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                        event: Message,
                        data: Dict[str, str]
                        ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)
        
        consoleLogger.middlewareStart()

        if event.text and event.text.startswith("/start"):
            async with self.pool.acquire() as conn:
                role = await conn.fetchval(
                    "select get_name_role_by_telegram_id($1)", event.from_user.id 
                )
            if role is None:
                consoleLogger.middlewareEndWithCode("Не присвоена роль")
                await event.answer("Не присвоена роль. Обратитесь к администратору.")
                return
            
            data["user_role"] = role
            consoleLogger.middlewareData("user_role", data["user_role"])
            consoleLogger.middlewareEnd()
            return await handler(event, data)
