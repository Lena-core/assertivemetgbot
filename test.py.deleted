#!/usr/bin/env python3
"""
Скрипт для тестирования основных компонентов бота
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_components():
    """Тестирование основных компонентов"""
    print("🧪 ТЕСТИРОВАНИЕ КОМПОНЕНТОВ ASSERTIVE.ME BOT")
    print("=" * 50)
    
    # Тест 0: Проверка версий библиотек
    print("0️⃣ Проверка версий библиотек...")
    try:
        import telegram
        import openai
        print(f"   ℹ️ python-telegram-bot: {telegram.__version__}")
        print(f"   ℹ️ openai: {openai.__version__}")
        print("   ✅ Библиотеки установлены")
    except Exception as e:
        print(f"   ❌ Ошибка с библиотеками: {e}")
        print("   ⚠️ Запустите: reinstall.bat")
        return False
    
    # Тест 1: Проверка конфигурации
    print("1️⃣ Тестирование конфигурации...")
    try:
        from config import TELEGRAM_BOT_TOKEN, OPENAI_API_KEY, MESSAGES
        assert TELEGRAM_BOT_TOKEN, "Telegram Bot Token не найден"
        assert OPENAI_API_KEY, "OpenAI API Key не найден"
        assert MESSAGES, "Сообщения не загружены"
        print("   ✅ Конфигурация загружена успешно")
    except Exception as e:
        print(f"   ❌ Ошибка конфигурации: {e}")
        return False
    
    # Тест 2: Проверка базы данных
    print("2️⃣ Тестирование базы данных...")
    try:
        from database import db_manager
        # Пробуем создать тестовую запись
        test_request_id = db_manager.save_request(
            user_id=12345,
            message_type='test',
            request_text='Тестовое сообщение',
            response_variants=['Вариант 1', 'Вариант 2', 'Вариант 3']
        )
        assert test_request_id, "Не удалось создать тестовый запрос"
        
        # Тестируем получение статистики
        stats = db_manager.get_user_stats()
        assert 'unique_users' in stats, "Неверная структура статистики"
        
        print("   ✅ База данных работает корректно")
    except Exception as e:
        print(f"   ❌ Ошибка базы данных: {e}")
        return False
    
    # Тест 3: Проверка валидатора
    print("3️⃣ Тестирование валидатора...")
    try:
        from validators import validator
        
        # Тест короткого сообщения
        is_valid, error = validator.is_valid_for_processing("Hi")
        assert not is_valid, "Короткое сообщение должно быть невалидным"
        
        # Тест токсичного сообщения
        is_valid, error = validator.is_valid_for_processing("Ты дурак, не понимаешь ничего!")
        assert is_valid, "Токсичное сообщение должно быть валидным"
        
        print("   ✅ Валидатор работает корректно")
    except Exception as e:
        print(f"   ❌ Ошибка валидатора: {e}")
        return False
    
    # Тест 4: Проверка LLM сервиса (только инициализация, без реального запроса)
    print("4️⃣ Тестирование LLM сервиса...")
    try:
        from llm_service import llm_service
        assert llm_service.client, "LLM клиент не инициализирован"
        
        # Тест форматирования
        test_variants = ["Вариант 1", "Вариант 2", "Вариант 3"]
        formatted = llm_service.format_variants_message(test_variants)
        assert "Вариант 1" in formatted, "Форматирование не работает"
        
        print("   ✅ LLM сервис инициализирован корректно")
    except Exception as e:
        print(f"   ❌ Ошибка LLM сервиса: {e}")
        return False
    
    # Тест 5: Проверка обработчика сообщений
    print("5️⃣ Тестирование обработчика сообщений...")
    try:
        from message_handler import message_handler
        assert message_handler, "Обработчик сообщений не инициализирован"
        print("   ✅ Обработчик сообщений загружен корректно")
    except Exception as e:
        print(f"   ❌ Ошибка обработчика: {e}")
        return False
    
    print("\n🎉 ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
    print("🚀 Бот готов к запуску!")
    return True

def test_real_llm():
    """Тест реального запроса к OpenAI (опционально)"""
    print("\n🔄 Тестирование реального запроса к OpenAI...")
    try:
        from llm_service import llm_service
        
        test_text = "Ты полный идиот, ничего не понимаешь!"
        variants = llm_service.generate_assertive_variants(test_text)
        
        if variants and len(variants) >= 1:
            print("   ✅ OpenAI API работает!")
            print("   📝 Пример сгенерированного варианта:")
            print(f"      '{variants[0]}'")
            return True
        else:
            print("   ❌ OpenAI API не вернул результаты")
            return False
    except Exception as e:
        print(f"   ❌ Ошибка OpenAIAPI: {e}")
        return False

if __name__ == "__main__":
    import asyncio
    
    # Запускаем основные тесты
    success = asyncio.run(test_components())
    
    if success:
        # Спрашиваем о тесте OpenAI
        response = input("\n❓ Хотите протестировать реальный запрос к OpenAI? (да/нет): ").lower()
        if response in ['да', 'yes', 'y', 'д']:
            test_real_llm()
    
    print(f"\n{'='*50}")
    print("💡 Для запуска бота используйте: python main.py")
    print("📊 Для просмотра статистики: python stats.py")
