from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from asyncpg import Pool

class AuthStates(StatesGroup):
    waiting_for_login = State()
    waiting_for_password = State()

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, pool: Pool, state: FSMContext):
    user_id = message.from_user.id

    async with pool.acquire() as conn:
        user = await conn.fetchrow(f"SELECT get_user_id_by_telegram_id($1)", user_id)
    
    if user[0] != None:
        await message.answer("✅ Вы уже авторизованы! Добро пожаловать.")
        await state.clear()  # на всякий случай сбрасываем состояние
    else:
        await message.answer("🔐 Вы не авторизованы.\nПожалуйста, введите ваш логин:")
        await state.set_state(AuthStates.waiting_for_login)


# Хэндлер: получение логина
@router.message(AuthStates.waiting_for_login, F.text)
async def process_login(message: types.Message, state: FSMContext):
    login = message.text.strip()
    await state.update_data(login=login)
    await message.answer("🔑 Теперь введите ваш пароль:")
    await state.set_state(AuthStates.waiting_for_password)


# Хэндлер: получение пароля
@router.message(AuthStates.waiting_for_password, F.text)
async def process_password(message: types.Message, state: FSMContext, pool: Pool):
    password = message.text.strip()
    data = await state.get_data()
    login = data.get("login")
    telegram_id = message.from_user.id

    async with pool.acquire() as conn:
        user = await conn.fetchrow(
            "SELECT id FROM users WHERE username = $1 AND password_hash = $2",
            login, password
        )
        if user != None:
            await conn.execute(f"call set_telegram_id_for_user($1, $2)", user[0], telegram_id)
            await message.answer("🎉 Авторизация успешна! Теперь вы можете пользоваться ботом.")
            await state.clear()
        else:
            await message.answer("❌ Неверный логин или пароль. Попробуйте снова.\nВведите логин:")
            await state.set_state(AuthStates.waiting_for_login)


