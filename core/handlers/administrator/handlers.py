from aiogram import Router, F, types

router = Router()

@router.message(F.text == "🛠️ Создать тикет")
async def create_ticket(message: types.Message, user_role: str):
    # Middleware гарантирует, что user_role — это 'teacher', 'admin' и т.д.
    if user_role != "administrator":
        # На всякий случай (хотя middleware + правильная маршрутизация должны этого избежать)
        return
    await message.answer("Опишите проблему...")