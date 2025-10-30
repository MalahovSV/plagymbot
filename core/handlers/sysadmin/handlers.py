
from aiogram import Router, types, F
from asyncpg import Pool
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from core.keyboards.role_keyboards import get_keyboard



# Состояния для FSM
class AddDeviceStates(StatesGroup):
    waiting_for_code = State()
    waiting_for_name = State()
    waiting_for_location = State()

class FindDeviceState(StatesGroup):
    waiting_for_code = State()


router = Router()

@router.message(F.text == "➕ Добавить устройство")
async def add_device_start(message: types.Message, user_role: str, state: FSMContext):
    print(user_role)
    if user_role != "sysadmin":
        print("Ошибка роли сисадмин")
        return 
    await message.answer("🔤 Введите код устройства:")
    await state.set_state(AddDeviceStates.waiting_for_code)

# === Хендлер: "🔍 Устройство по коду" ===
@router.message(F.text == "🔍 Устройство по коду")
async def find_device_start(message: types.Message, user_role: str, state: FSMContext):
    print(user_role)
    if user_role != "sysadmin":
        return
    await message.answer("🔤 Введите код устройства для поиска:")
    await state.set_state(FindDeviceState.waiting_for_code)


@router.message(FindDeviceState.waiting_for_code)
async def find_device_by_code(message: types.Message, state: FSMContext, pool: Pool, user_role: str):
    print(user_role)
    if user_role != "sysadmin":
        await state.clear()
        return

    code = message.text.strip()
    async with pool.acquire() as conn:
        device = await conn.fetchrow(
            "SELECT name, location FROM devices WHERE device_code = $1", code
        )

    if device:
        await message.answer(
            f"✅ Найдено устройство:\n\n"
            f"Код: {code}\n"
            f"Название: {device['name']}\n"
            f"Расположение: {device['location']}",
            reply_markup=get_keyboard("sysadmin")
        )
    else:
        await message.answer("❌ Устройство с таким кодом не найдено.", reply_markup=get_keyboard("sysadmin"))

    await state.clear()


# === Хендлер: "🎫 Текущие тикеты" ===
@router.message(F.text == "🎫 Текущие тикеты")
async def show_current_tickets(message: types.Message, user_role: str, pool: Pool):
    if user_role != "sysadmin":
        return

    async with pool.acquire() as conn:
        tickets = await conn.fetch(
            """
            SELECT t.id, u.username, t.device_code, t.description, t.created_at
            FROM tickets t
            JOIN users u ON t.user_id = u.id
            WHERE t.status = 'open'
            ORDER BY t.created_at DESC
            LIMIT 10
            """
        )

    if not tickets:
        await message.answer("📭 Нет открытых тикетов.", reply_markup=get_keyboard("sysadmin"))
    else:
        response = "🎫 Открытые тикеты:\n\n"
        for t in tickets:
            dev = t["device_code"] or "—"
            desc = (t["description"][:60] + "...") if len(t["description"]) > 60 else t["description"]
            response += f"ID: {t['id']} | От: {t['username']}\nУстройство: {dev}\nОписание: {desc}\n\n"
        await message.answer(response, reply_markup=get_keyboard("sysadmin"))


# === Хендлер: "🚪 Выйти" (можно вынести в common, но дублирование допустимо) ===
@router.message(F.text == "🚪 Выйти")
async def logout(message: types.Message, pool: Pool, state: FSMContext):
    # Сбрасываем состояние
    await state.clear()
    # Отвязываем telegram_id
    async with pool.acquire() as conn:
        await conn.execute("UPDATE users SET telegram_id = NULL WHERE telegram_id = $1", message.from_user.id)
    
    from aiogram.types import ReplyKeyboardRemove
    await message.answer("Вы вышли из системы.", reply_markup=ReplyKeyboardRemove())
    await message.answer("Для входа напишите /start")



