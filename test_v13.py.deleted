#!/usr/bin/env python3
"""
Тест для версии 13.x
"""
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def test_v13_components():
    """Тестирование компонентов версии 13.x"""
    print("🧪 ТЕСТ КОМПОНЕНТОВ v13.x")
    print("=" * 30)
    
    # Тест 1: Импорт telegram
    try:
        import telegram
        print(f"✅ telegram: {telegram.__version__}")
        assert telegram.__version__.startswith('13.'), f"Неправильная версия: {telegram.__version__}"
    except Exception as e:
        print(f"❌ Ошибка telegram: {e}")
        return False
    
    # Тест 2: Импорт telegram.ext
    try:
        from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
        print("✅ telegram.ext компоненты импортированы")
    except Exception as e:
        print(f"❌ Ошибка telegram.ext: {e}")
        return False
    
    # Тест 3: Импорт openai
    try:
        import openai
        print(f"✅ openai: {openai.version.VERSION}")
        assert openai.version.VERSION.startswith('0.28'), f"Неправильная версия: {openai.version.VERSION}"
    except Exception as e:
        print(f"❌ Ошибка openai: {e}")
        return False
    
    # Тест 4: Импорт config
    try:
        from config import TELEGRAM_BOT_TOKEN, OPENAI_API_KEY
        print("✅ config импортирован")
        print(f"   Telegram токен: {TELEGRAM_BOT_TOKEN[:10]}...")
        print(f"   OpenAI ключ: {OPENAI_API_KEY[:20]}...")
    except Exception as e:
        print(f"❌ Ошибка config: {e}")
        return False
    
    # Тест 5: Создание Updater
    try:
        updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
        print("✅ Updater создан успешно")
    except Exception as e:
        print(f"❌ Ошибка создания Updater: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Тест 6: Импорт llm_service_v13
    try:
        from llm_service_v13 import llm_service_v13
        print("✅ llm_service_v13 импортирован")
    except Exception as e:
        print(f"❌ Ошибка llm_service_v13: {e}")
        return False
    
    # Тест 7: Импорт других компонентов
    try:
        from validators import validator
        from database import db_manager
        print("✅ validators и database импортированы")
    except Exception as e:
        print(f"❌ Ошибка дополнительных компонентов: {e}")
        return False
    
    print("\n🎉 ВСЕ ТЕСТЫ v13.x ПРОШЛИ УСПЕШНО!")
    return True

def test_openai_connection():
    """Тест подключения к OpenAI"""
    print("\n🔌 ТЕСТ OPENAI API...")
    try:
        from llm_service_v13 import llm_service_v13
        
        # Тестовое сообщение
        test_text = "Ты дурак, ничего не понимаешь!"
        
        print(f"Отправляем тест: '{test_text}'")
        variants = llm_service_v13.generate_assertive_variants(test_text)
        
        if variants and len(variants) >= 1:
            print("✅ OpenAI API работает!")
            print("📝 Пример варианта:")
            print(f"   '{variants[0]}'")
            return True
        else:
            print("❌ OpenAI API не вернул результаты")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка OpenAI API: {e}")
        return False

if __name__ == "__main__":
    print("🚀 ТЕСТИРОВАНИЕ ВЕРСИИ 13.x")
    print("=" * 40)
    
    # Основные тесты
    components_ok = test_v13_components()
    
    if components_ok:
        response = input("\n❓ Протестировать реальный запрос к OpenAI? (да/нет): ").lower()
        if response in ['да', 'yes', 'y', 'д']:
            openai_ok = test_openai_connection()
        else:
            openai_ok = True
            print("⏭️ Тест OpenAI пропущен")
    else:
        openai_ok = False
    
    print(f"\n{'='*40}")
    if components_ok and openai_ok:
        print("🎉 ВСЕ ГОТОВО К ЗАПУСКУ!")
        print("💡 Запустите: python main_v13_full.py")
    else:
        print("❌ Найдены проблемы!")
        if not components_ok:
            print("   - Проблемы с компонентами")
        if not openai_ok:
            print("   - Проблемы с OpenAI API")
