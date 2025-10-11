
from aiogram import Router, types, F
from asyncpg import Pool
from aiogram.fsm.state import State, StatesGroup

class sysadminState(StatesGroup):
    choosing_button_from_menu = State()


router = Router()

@router.message(F.text == "🛠️ Создать тикет")
async def create_ticket(message: types.Message, user_role: str):
    # Middleware гарантирует, что user_role — это 'teacher', 'admin' и т.д.
    if user_role != "teacher":
        # На всякий случай (хотя middleware + правильная маршрутизация должны этого избежать)
        return
    await message.answer("Опишите проблему...")


