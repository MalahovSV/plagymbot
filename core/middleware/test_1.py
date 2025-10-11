from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable

class MyMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Код до обработчика
        print("До обработчика")

        # Вызываем следующий обработчик (или следующую мидлварь)
        result = await handler(event, data)

        # Код после обработчика
        print("После обработчика")

        return result