# handlers/debug_fallback.py
from aiogram import Router, F, types

router = Router()

@router.message(F.text)
async def debug_all(message: types.Message):
    print(f"🔍 DEBUG: Получено сообщение: '{message.text}'")
    user_role = "test"
    print(f"🔍 DEBUG: user_role = {repr(user_role)} (тип: {type(user_role)})")
    await message.answer(f"Отладка: роль = {user_role}")