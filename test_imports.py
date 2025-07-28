#!/usr/bin/env python3
"""
Тест импортов для отладки
"""

print("🧪 ТЕСТ ИМПОРТОВ")
print("=" * 20)

# Тест 1: Базовый импорт telegram
try:
    import telegram
    print("✅ import telegram - OK")
    print(f"   Версия: {telegram.__version__}")
except Exception as e:
    print(f"❌ import telegram - FAIL: {e}")
    exit(1)

# Тест 2: Импорт telegram.ext
try:
    from telegram.ext import Application
    print("✅ from telegram.ext import Application - OK")
except Exception as e:
    print(f"❌ from telegram.ext import Application - FAIL: {e}")
    exit(1)

# Тест 3: Импорт всех нужных компонентов
try:
    from telegram.ext import CommandHandler, MessageHandler, filters, CallbackQueryHandler
    print("✅ Все обработчики импортированы - OK")
except Exception as e:
    print(f"❌ Ошибка импорта обработчиков: {e}")
    exit(1)

# Тест 4: Импорт config
try:
    from config import TELEGRAM_BOT_TOKEN
    print("✅ config импортирован - OK")
    print(f"   Токен: {TELEGRAM_BOT_TOKEN[:10]}...")
except Exception as e:
    print(f"❌ Ошибка импорта config: {e}")
    exit(1)

# Тест 5: Создание Application
try:
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    print("✅ Application создан - OK")
except Exception as e:
    print(f"❌ Ошибка создания Application: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n🎉 ВСЕ ИМПОРТЫ РАБОТАЮТ!")
print("💡 Проблема должна быть в другом месте...")
