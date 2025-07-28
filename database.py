import sqlite3
import json
from datetime import datetime
from config import DATABASE_PATH

class DatabaseManager:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных и создание таблиц"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Создаем таблицу для метрик запросов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                timestamp DATETIME NOT NULL,
                message_type TEXT NOT NULL,
                source_chat_id INTEGER,
                source_chat_type TEXT,
                source_chat_title TEXT,
                request_text TEXT NOT NULL,
                response_variants TEXT NOT NULL,
                selected_variant_index INTEGER,
                feedback_reason TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_request(self, user_id, message_type, request_text, response_variants, 
                    source_chat_id=None, source_chat_type=None, source_chat_title=None):
        """Сохранение запроса пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO requests (
                user_id, timestamp, message_type, source_chat_id, 
                source_chat_type, source_chat_title, request_text, response_variants
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id, datetime.now(), message_type, source_chat_id,
            source_chat_type, source_chat_title, request_text, 
            json.dumps(response_variants, ensure_ascii=False)
        ))
        
        request_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return request_id
    
    def save_feedback(self, request_id, selected_variant_index=None, feedback_reason=None):
        """Сохранение обратной связи от пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE requests 
            SET selected_variant_index = ?, feedback_reason = ?
            WHERE id = ?
        ''', (selected_variant_index, feedback_reason, request_id))
        
        conn.commit()
        conn.close()
    
    def get_user_stats(self):
        """Получение статистики пользователей"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Количество уникальных пользователей
        cursor.execute('SELECT COUNT(DISTINCT user_id) FROM requests')
        unique_users = cursor.fetchone()[0]
        
        # Общее количество запросов
        cursor.execute('SELECT COUNT(*) FROM requests')
        total_requests = cursor.fetchone()[0]
        
        # Статистика по типам сообщений
        cursor.execute('''
            SELECT message_type, COUNT(*) 
            FROM requests 
            GROUP BY message_type
        ''')
        message_types = cursor.fetchall()
        
        # Топ чатов-источников
        cursor.execute('''
            SELECT source_chat_title, source_chat_id, COUNT(*) as count
            FROM requests 
            WHERE source_chat_id IS NOT NULL
            GROUP BY source_chat_id, source_chat_title
            ORDER BY count DESC
            LIMIT 10
        ''')
        top_chats = cursor.fetchall()
        
        conn.close()
        
        return {
            'unique_users': unique_users,
            'total_requests': total_requests,
            'message_types': dict(message_types),
            'top_chats': top_chats
        }

# Глобальный экземпляр менеджера базы данных
db_manager = DatabaseManager()
