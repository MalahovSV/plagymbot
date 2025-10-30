from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_keyboard(role: str) -> ReplyKeyboardMarkup:
    if role == "teacher":
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📝 Создать опрос"), KeyboardButton(text="🛠️ Создать тикет")],
                [KeyboardButton(text="📊 Мои опросы"), KeyboardButton(text="🚪 Выйти")]
            ],
            resize_keyboard=True
        )
    elif role == "student":
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🗳️ Пройти опрос"), KeyboardButton(text="📈 Мои результаты")],
                [KeyboardButton(text="🚪 Выйти")]
            ],
            resize_keyboard=True
        )
    elif role == "admin":
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🛠️ Создать тикет"), KeyboardButton(text="📊 Отчёты")],
                [KeyboardButton(text="👥 Управление"), KeyboardButton(text="🚪 Выйти")]
            ],
            resize_keyboard=True
        )
    elif role == "sysadmin":
        return ReplyKeyboardMarkup(
                       keyboard=[
                [KeyboardButton(text="➕ Добавить устройство")],
                [KeyboardButton(text="🔍 Устройство по коду")],
                [KeyboardButton(text="🎫 Текущие тикеты")],
                [KeyboardButton(text="🚪 Выйти")]            
                ],
            resize_keyboard=True
        )
    else:
        return ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="🔐 /start")]],
            resize_keyboard=True
        )