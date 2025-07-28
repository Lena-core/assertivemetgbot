#!/usr/bin/env python3
"""
Тест простой стабильной версии
"""
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def test_simple_version():
    """Тестирование простой версии"""
    print("🧪 ТЕСТ ПРОСТОЙ СТАБИЛЬНОЙ ВЕРСИИ")
    print("=" * 35)
    
    # Тест 1: Импорт основных библиотек
    try:
        import requests
        print(f"✅ requests: {requests.__version__}")
    except Exception as e:
        print(f"❌ Ошибка requests: {e}")
        return False
    
    try:
        import openai
        print(f"✅ openai: {openai.version.VERSION}")
    except Exception as e:
        print(f"❌ Ошибка openai: {e}")
        return False
    
    try:
        import dotenv
        print("✅ python-dotenv работает")
    except Exception as e:
        print(f"❌ Ошибка dotenv: {e}")
        return False
    
    # Тест 2: Импорт конфигурации
    try:
        from config import TELEGRAM_BOT_TOKEN, OPENAI_API_KEY
        print("✅ config импортирован")
        print(f"   Telegram токен: {TELEGRAM_BOT_TOKEN[:10]}...")
        print(f"   OpenAI ключ: {OPENAI_API_KEY[:20]}...")
    except Exception as e:
        print(f"❌ Ошибка config: {e}")
        return False
    
    # Тест 3: Другие компоненты
    try:
        from validators import validator
        from database import db_manager
        print("✅ validators и database импортированы")
    except Exception as e:
        print(f"❌ Ошибка дополнительных компонентов: {e}")
        return False
    
    # Тест 4: Проверка Telegram API
    try:
        api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
        response = requests.get(api_url, timeout=10)
        if response.json().get('ok'):
            bot_info = response.json()['result']
            print(f"✅ Telegram API работает: @{bot_info['username']}")
        else:
            print("❌ Telegram API не отвечает")
            return False
    except Exception as e:
        print(f"❌ Ошибка Telegram API: {e}")
        return False
    
    print("\n🎉 ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
    return True

def test_openai_simple():
    """Тест OpenAI API"""
    print("\n🔌 ТЕСТ OPENAI API...")
    try:
        import openai
        from config import OPENAI_API_KEY
        
        openai.api_key = OPENAI_API_KEY
        
        # Простой тестовый запрос
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Скажи просто 'Привет'"}
            ],
            max_tokens=10
        )
        
        if response and response['choices']:
            result = response['choices'][0]['message']['content']
            print(f"✅ OpenAI API работает! Ответ: '{result.strip()}'")
            return True
        else:
            print("❌ OpenAI API не вернул результат")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка OpenAI API: {e}")
        return False

if __name__ == "__main__":
    print("🚀 ТЕСТИРОВАНИЕ ПРОСТОЙ ВЕРСИИ")
    print("=" * 40)
    
    # Основные тесты
    components_ok = test_simple_version()
    
    if components_ok:
        response = input("\n❓ Протестировать реальный запрос к OpenAI? (да/нет): ").lower()
        if response in ['да', 'yes', 'y', 'д']:
            openai_ok = test_openai_simple()
        else:
            openai_ok = True
            print("⏭️ Тест OpenAI пропущен")
    else:
        openai_ok = False
    
    print(f"\n{'='*40}")
    if components_ok and openai_ok:
        print("🎉 ВСЕ ГОТОВО К ЗАПУСКУ!")
        print("💡 Запустите: python main_simple_stable.py")
    else:
        print("❌ Найдены проблемы!")
        if not components_ok:
            print("   - Проблемы с компонентами")
        if not openai_ok:
            print("   - Проблемы с OpenAI API")
