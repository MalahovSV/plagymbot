from aiogram import Router, F, types

router = Router()

@router.message(F.text == "🛠️ Создать тикет")
async def create_ticket(message: types.Message, user_role: str):
    # Middleware гарантирует, что user_role — это 'technician', 'admin' и т.д.
    if user_role != "technician":
        # На всякий случай (хотя middleware + правильная маршрутизация должны этого избежать)
        return
    await message.answer("Опишите проблему...")