#!/usr/bin/env python3
"""
Скрипт для просмотра статистики использования бота
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import db_manager
from datetime import datetime
import json

def print_stats():
    """Вывод статистики использования бота"""
    print("=" * 50)
    print("📊 СТАТИСТИКА ASSERTIVE.ME BOT")
    print("=" * 50)
    
    try:
        stats = db_manager.get_user_stats()
        
        print(f"👥 Уникальных пользователей: {stats['unique_users']}")
        print(f"📝 Всего запросов: {stats['total_requests']}")
        print()
        
        print("📊 Распределение по типам сообщений:")
        for msg_type, count in stats['message_types'].items():
            print(f"  • {msg_type}: {count}")
        print()
        
        print("🏆 ТОП-10 чатов-источников пересылок:")
        if stats['top_chats']:
            for i, (title, chat_id, count) in enumerate(stats['top_chats'], 1):
                title_display = title if title else f"Chat {chat_id}"
                print(f"  {i}. {title_display}: {count} сообщений")
        else:
            print("  Нет данных о пересылках")
        
        print()
        print(f"📅 Отчет сгенерирован: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ Ошибка при получении статистики: {e}")

def export_stats_json():
    """Экспорт статистики в JSON файл"""
    try:
        stats = db_manager.get_user_stats()
        
        # Подготавливаем данные для JSON
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'unique_users': stats['unique_users'],
            'total_requests': stats['total_requests'],
            'message_types': stats['message_types'],
            'top_chats': [
                {
                    'title': title,
                    'chat_id': chat_id,
                    'count': count
                }
                for title, chat_id, count in stats['top_chats']
            ]
        }
        
        filename = f"stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Статистика экспортирована в файл: {filename}")
        
    except Exception as e:
        print(f"❌ Ошибка при экспорте: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--export":
        export_stats_json()
    else:
        print_stats()
        print("\n💡 Для экспорта в JSON используйте: python stats.py --export")
