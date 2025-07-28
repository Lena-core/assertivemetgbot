#!/usr/bin/env python3
"""
Проверка зависимостей и их версий
"""

def check_dependencies():
    """Детальная проверка всех зависимостей"""
    print("🔍 ПРОВЕРКА ЗАВИСИМОСТЕЙ")
    print("=" * 40)
    
    # Проверяем основные импорты
    try:
        print("📦 Проверяем импорты...")
        
        import telegram
        print(f"✅ telegram: {telegram.__version__}")
        
        from telegram.ext import Application
        print("✅ Application импортирован")
        
        from telegram.ext import CommandHandler, MessageHandler, filters
        print("✅ Обработчики импортированы")
        
        import openai
        print(f"✅ openai: {openai.__version__}")
        
        import dotenv
        print(f"✅ python-dotenv: {dotenv.__version__}")
        
    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")
        return False
    
    # Проверяем конфликты версий
    print("\n🔍 Проверяем конфликты...")
    try:
        import pkg_resources
        installed_packages = [d for d in pkg_resources.working_set]
        
        telegram_packages = [p for p in installed_packages if 'telegram' in p.project_name.lower()]
        for pkg in telegram_packages:
            print(f"📦 {pkg.project_name}: {pkg.version}")
            
    except Exception as e:
        print(f"⚠️ Не удалось проверить версии: {e}")
    
    # Тест создания Application
    print("\n🧪 Тестируем создание Application...")
    try:
        from config import TELEGRAM_BOT_TOKEN
        from telegram.ext import Application
        
        app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        print("✅ Application создается без ошибок")
        
        # Тест добавления обработчика
        from telegram.ext import CommandHandler
        
        async def dummy_handler(update, context):
            pass
            
        app.add_handler(CommandHandler("test", dummy_handler))
        print("✅ Обработчик добавляется без ошибок")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при создании Application: {e}")
        import traceback
        print("📜 Traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = check_dependencies()
    if success:
        print("\n🎉 Все проверки прошли! Попробуйте minimal_test.py")
    else:
        print("\n💥 Найдены проблемы с зависимостями!")
