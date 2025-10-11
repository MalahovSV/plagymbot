import os
import importlib
from pathlib import Path
from aiogram import Router

all_routers = []

handlers_dir = Path(__file__).parent

for item in handlers_dir.iterdir():
    if item.is_dir() and not item.name.startswith("__"):
        handler_file = item / "handlers.py"
        if handler_file.exists():
            module_name = f"core.handlers.{item.name}.handlers"
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "router") and isinstance(module.router, Router):
                    all_routers.append(module.router)
                    print(f"✅ Загружен роутер: {module_name}")
                else:
                    print(f"⚠️  В {module_name} не найден роутер")
            except Exception as e:
                print(f"❌ Ошибка при загрузке {module_name}: {e}")

try:
    from .authorization import router as auth_router
    #from .common import router as common_router
    all_routers.insert(0, auth_router)   # auth — первый
    #all_routers.insert(1, common_router) # common — второй

except Exception as e:
    print(f"❌ Ошибка загрузки базовых хендлеров: {e}")
