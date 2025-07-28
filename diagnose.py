#!/usr/bin/env python3
"""
Скрипт диагностики Telegram бота
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import TELEGRAM_BOT_TOKEN
from telegram import Bot
from telegram.error import TelegramError

async def test_bot_connection():
    """Тестирование подключения к Telegram API"""
    print("🔍 ДИАГНОСТИКА TELEGRAM БОТА")
    print("=" * 40)
    
    try:
        # Создаем бота
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        # Тест 1: Проверяем токен
        print("1️⃣ Проверка токена...")
        me = await bot.get_me()
        print(f"   ✅ Токен корректный!")
        print(f"   🤖 Имя бота: {me.first_name}")
        print(f"   📝 Username: @{me.username}")
        print(f"   🆔 ID: {me.id}")
        
        # Тест 2: Проверяем права
        print("\n2️⃣ Проверка прав...")
        try:
            # Пробуем получить обновления
            updates = await bot.get_updates(limit=1)
            print(f"   ✅ Права на получение обновлений: OK")
            print(f"   📊 Количество необработанных обновлений: {len(updates)}")
        except Exception as e:
            print(f"   ❌ Ошибка получения обновлений: {e}")
        
        # Тест 3: Проверяем команды
        print("\n3️⃣ Проверка команд бота...")
        try:
            commands = await bot.get_my_commands()
            print(f"   📋 Установленных команд: {len(commands)}")
            for cmd in commands:
                print(f"      /{cmd.command} - {cmd.description}")
        except Exception as e:
            print(f"   ⚠️ Ошибка получения команд: {e}")
        
        # Тест 4: Проверяем webhook
        print("\n4️⃣ Проверка webhook...")
        try:
            webhook_info = await bot.get_webhook_info()
            if webhook_info.url:
                print(f"   ⚠️ Установлен webhook: {webhook_info.url}")
                print("   💡 Для polling нужно удалить webhook!")
                
                # Удаляем webhook
                await bot.delete_webhook()
                print("   ✅ Webhook удален")
            else:
                print("   ✅ Webhook не установлен (нужно для polling)")
        except Exception as e:
            print(f"   ❌ Ошибка проверки webhook: {e}")
        
        print("\n🎯 РЕЗУЛЬТАТ: Подключение к Telegram API работает!")
        return True
        
    except TelegramError as e:
        print(f"\n❌ ОШИБКА TELEGRAM API: {e}")
        if "Unauthorized" in str(e):
            print("💡 Возможные причины:")
            print("   - Неверный токен бота")
            print("   - Бот был удален или заблокирован")
        return False
    except Exception as e:
        print(f"\n❌ НЕОЖИДАННАЯ ОШИБКА: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_bot_connection())
    if result:
        print("\n✅ Диагностика прошла успешно!")
        print("💡 Если бот все еще не отвечает, проверьте обработчики сообщений")
    else:
        print("\n❌ Найдены проблемы с подключением!")
