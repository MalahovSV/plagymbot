import os
import importlib
from pathlib import Path
from aiogram import Router

# Создаём главный роутер или список
all_routers = []

# Путь к текущей директории (handlers/)
handlers_dir = Path(__file__).parent

# Проходим по всем подпапкам в handlers/
for item in handlers_dir.iterdir():
    if item.is_dir() and not item.name.startswith("__"):
        handler_file = item / "handlers.py"
        if handler_file.exists():
            # Формируем имя модуля: handlers.teacher.handlers
            module_name = f"handlers.{item.name}.handlers"
            try:
                module = importlib.import_module(module_name)
                # Ищем атрибут `router` в модуле
                if hasattr(module, "router") and isinstance(module.router, Router):
                    all_routers.append(module.router)
                    print(f"✅ Загружен роутер: {module_name}")
                else:
                    print(f"⚠️  В {module_name} не найден роутер")
            except Exception as e:
                print(f"❌ Ошибка при загрузке {module_name}: {e}")

# Также подключаем authorization и common вручную (они не в подпапках)
try:
    from .authorization import router as auth_router
    #from .common import router as common_router
    all_routers.insert(0, auth_router)   # auth — первый
    #all_routers.insert(1, common_router) # common — второй
except Exception as e:
    print(f"❌ Ошибка загрузки базовых хендлеров: {e}")