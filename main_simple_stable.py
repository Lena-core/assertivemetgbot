#!/usr/bin/env python3
"""
Простая стабильная версия Assertive.Me бота 
Использует прямые HTTP запросы к Telegram Bot API
"""
import requests
import json
import time
import logging
from threading import Thread
import openai

from config import TELEGRAM_BOT_TOKEN, OPENAI_API_KEY, MESSAGES
from validators import validator
from database import db_manager

# Настройка OpenAI для версии 0.28.x
openai.api_key = OPENAI_API_KEY

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class SimpleTelegramBot:
    def __init__(self, token):
        self.token = token
        self.api_url = f"https://api.telegram.org/bot{token}"
        self.last_update_id = 0
        self.user_requests = {}
        self.processing_messages = {}
    
    def send_message(self, chat_id, text, reply_markup=None, parse_mode=None):
        """Отправка сообщения"""
        url = f"{self.api_url}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': text
        }
        
        if reply_markup:
            data['reply_markup'] = json.dumps(reply_markup)
        
        if parse_mode:
            data['parse_mode'] = parse_mode
        
        try:
            response = requests.post(url, data=data)
            return response.json()
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения: {e}")
            return None
    
    def edit_message_text(self, chat_id, message_id, text):
        """Редактирование сообщения"""
        url = f"{self.api_url}/editMessageText"
        data = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': text
        }
        
        try:
            response = requests.post(url, data=data)
            return response.json()
        except Exception as e:
            logger.error(f"Ошибка редактирования сообщения: {e}")
            return None
    
    def delete_message(self, chat_id, message_id):
        """Удаление сообщения"""
        url = f"{self.api_url}/deleteMessage"
        data = {
            'chat_id': chat_id,
            'message_id': message_id
        }
        
        try:
            response = requests.post(url, data=data)
            return response.json()
        except Exception as e:
            logger.error(f"Ошибка удаления сообщения: {e}")
            return None
    
    def answer_callback_query(self, callback_query_id):
        """Ответ на callback query"""
        url = f"{self.api_url}/answerCallbackQuery"
        data = {'callback_query_id': callback_query_id}
        
        try:
            response = requests.post(url, data=data)
            return response.json()
        except Exception as e:
            logger.error(f"Ошибка ответа на callback: {e}")
            return None
    
    def get_updates(self, offset=None, timeout=30):
        """Получение обновлений"""
        url = f"{self.api_url}/getUpdates"
        data = {'timeout': timeout}
        
        if offset:
            data['offset'] = offset
        
        try:
            response = requests.post(url, data=data, timeout=timeout + 5)
            return response.json()
        except Exception as e:
            logger.error(f"Ошибка получения обновлений: {e}")
            return None
    
    def generate_assertive_variants(self, text):
        """Генерация ассертивных вариантов через OpenAI"""
        try:
            prompt = f"""Переформулируй следующий комментарий в 3 ассертивных вариантах. Фокусируйся на 'Я-сообщениях' и конструктивном тоне, избегая обвинений. Если это чей-то комментарий, предложи варианты ассертивного ответа на него. Если это черновик пользователя, предложи ассертивные способы выразить ту же мысль. 

Оригинальный комментарий: '{text}'

Ответь в формате:
1. [первый вариант]
2. [второй вариант]  
3. [третий вариант]"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Ты эксперт по ассертивной коммуникации. Твоя задача - помочь людям выражать свои мысли конструктивно и без агрессии. Всегда предлагай именно 3 варианта переформулировки, используя 'Я-сообщения' и избегая обвинений."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            content = response['choices'][0]['message']['content'].strip()
            variants = self._parse_variants(content)
            
            return variants[:3] if variants else None
            
        except Exception as e:
            logger.error(f"Ошибка при обращении к OpenAI: {e}")
            return None
    
    def _parse_variants(self, content):
        """Парсинг вариантов из ответа GPT"""
        import re
        variants = []
        
        # Пытаемся найти пронумерованные варианты
        pattern = r'^\s*(\d+)\.?\s*(.+?)(?=^\s*\d+\.|\Z)'
        matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            variant = match[1].strip()
            if variant:
                variants.append(variant)
        
        # Если не нашли, разбиваем по строкам
        if len(variants) < 3:
            lines = content.split('\n')
            variants = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith(('Вариант', 'Ответ', 'Переформулировка')):
                    line = re.sub(r'^\d+\.?\s*', '', line)
                    if len(line) > 10:
                        variants.append(line)
        
        return variants[:3]
    
    def format_variants_message(self, variants):
        """Форматирование вариантов для отправки"""
        if not variants:
            return "Извините, не удалось сгенерировать варианты переформулировки."
        
        message = "✨ Вот 3 ассертивных варианта переформулировки:\n\n"
        
        for i, variant in enumerate(variants, 1):
            message += f"**{i}.** {variant}\n\n"
        
        message += "Выберите наиболее подходящий вариант или укажите, что ни один не подошел:"
        
        return message
    
    def create_feedback_keyboard(self, variants_count):
        """Создание клавиатуры для обратной связи"""
        keyboard = []
        for i in range(variants_count):
            keyboard.append([{"text": f"Выбрать {i+1}", "callback_data": f"select_{i+1}"}])
        
        keyboard.append([{"text": "Ни один не подошел", "callback_data": "select_none"}])
        
        return {"inline_keyboard": keyboard}
    
    def process_message(self, chat_id, message_id, user_id, text, message_type='direct_text', 
                       source_chat_id=None, source_chat_type=None, source_chat_title=None):
        """Обработка сообщения"""
        logger.info(f"📝 Обрабатываем сообщение от {user_id}: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        
        # Отправляем сообщение о обработке
        processing_response = self.send_message(chat_id, MESSAGES['processing'])
        if processing_response and processing_response.get('ok'):
            self.processing_messages[user_id] = processing_response['result']['message_id']
        
        # Валидация
        clean_text = validator.clean_text(text)
        is_valid, validation_error = validator.is_valid_for_processing(clean_text)
        
        if not is_valid:
            # Удаляем сообщение "обрабатывается"
            if user_id in self.processing_messages:
                self.delete_message(chat_id, self.processing_messages[user_id])
            
            if validation_error == "too_long":
                self.send_message(chat_id, MESSAGES['too_long'])
            elif validation_error in ["too_short", "not_toxic"]:
                self.send_message(chat_id, MESSAGES['too_short_or_non_toxic'])
            return
        
        # Генерируем варианты
        variants = self.generate_assertive_variants(clean_text)
        
        if not variants:
            # Удаляем сообщение "обрабатывается"
            if user_id in self.processing_messages:
                self.delete_message(chat_id, self.processing_messages[user_id])
            self.send_message(chat_id, MESSAGES['error'])
            return
        
        # Сохраняем в базу данных
        try:
            request_id = db_manager.save_request(
                user_id=user_id,
                message_type=message_type,
                request_text=clean_text,
                response_variants=variants,
                source_chat_id=source_chat_id,
                source_chat_type=source_chat_type,
                source_chat_title=source_chat_title
            )
            
            self.user_requests[user_id] = request_id
        except Exception as e:
            logger.error(f"Ошибка сохранения в БД: {e}")
        
        # Удаляем сообщение "обрабатывается"
        if user_id in self.processing_messages:
            self.delete_message(chat_id, self.processing_messages[user_id])
        
        # Отправляем варианты с кнопками
        message_text = self.format_variants_message(variants)
        keyboard = self.create_feedback_keyboard(len(variants))
        
        self.send_message(chat_id, message_text, reply_markup=keyboard, parse_mode='Markdown')
    
    def handle_callback_query(self, callback_query):
        """Обработка callback query"""
        query_id = callback_query['id']
        user_id = callback_query['from']['id']
        chat_id = callback_query['message']['chat']['id']
        message_id = callback_query['message']['message_id']
        callback_data = callback_query['data']
        
        # Подтверждаем callback
        self.answer_callback_query(query_id)
        
        # Получаем ID запроса
        request_id = self.user_requests.get(user_id)
        if not request_id:
            self.edit_message_text(chat_id, message_id, "Ошибка: запрос не найден.")
            return
        
        original_text = callback_query['message']['text']
        
        if callback_data.startswith("select_"):
            if callback_data == "select_none":
                # Пользователь выбрал "Ни один не подошел"
                new_text = original_text + "\n\n" + MESSAGES['feedback_request']
                self.edit_message_text(chat_id, message_id, new_text)
                # Здесь можно добавить логику ожидания причины
            else:
                # Пользователь выбрал один из вариантов
                variant_index = int(callback_data.split("_")[1])
                
                # Сохраняем выбор в базу данных
                try:
                    db_manager.save_feedback(request_id, selected_variant_index=variant_index)
                except Exception as e:
                    logger.error(f"Ошибка сохранения feedback: {e}")
                
                new_text = original_text + f"\n\n✅ Вы выбрали вариант {variant_index}. " + MESSAGES['feedback_thanks']
                self.edit_message_text(chat_id, message_id, new_text)
                
                # Удаляем связь
                if user_id in self.user_requests:
                    del self.user_requests[user_id]
    
    def handle_update(self, update):
        """Обработка одного обновления"""
        try:
            if 'message' in update:
                message = update['message']
                chat_id = message['chat']['id']
                message_id = message['message_id']
                user_id = message['from']['id']
                
                # Команда /start
                if message.get('text') == '/start':
                    self.send_message(chat_id, MESSAGES['welcome'], parse_mode='Markdown')
                    return
                
                # Текстовые сообщения
                if 'text' in message:
                    text = message['text']
                    
                    # Игнорируем команды
                    if text.startswith('/'):
                        return
                    
                    # Определяем тип сообщения
                    message_type = 'direct_text'
                    source_chat_id = None
                    source_chat_type = None
                    source_chat_title = None
                    
                    if 'forward_from_chat' in message:
                        message_type = 'forwarded_message'
                        forward_chat = message['forward_from_chat']
                        source_chat_id = forward_chat['id']
                        source_chat_type = forward_chat['type']
                        source_chat_title = forward_chat.get('title')
                    
                    # Обрабатываем сообщение в отдельном потоке
                    thread = Thread(target=self.process_message, args=(
                        chat_id, message_id, user_id, text, message_type,
                        source_chat_id, source_chat_type, source_chat_title
                    ))
                    thread.start()
            
            elif 'callback_query' in update:
                self.handle_callback_query(update['callback_query'])
                
        except Exception as e:
            logger.error(f"Ошибка обработки обновления: {e}")
    
    def run(self):
        """Запуск бота"""
        logger.info("🚀 Запуск Simple Telegram Bot...")
        
        # Проверяем токен
        me_response = requests.get(f"{self.api_url}/getMe")
        if not me_response.json().get('ok'):
            logger.error("❌ Неверный токен бота!")
            return
        
        bot_info = me_response.json()['result']
        logger.info(f"✅ Бот запущен: @{bot_info['username']}")
        
        while True:
            try:
                # Получаем обновления
                updates_response = self.get_updates(offset=self.last_update_id + 1)
                
                if not updates_response or not updates_response.get('ok'):
                    time.sleep(1)
                    continue
                
                updates = updates_response['result']
                
                for update in updates:
                    self.last_update_id = update['update_id']
                    self.handle_update(update)
                
                if not updates:
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                logger.info("👋 Получен сигнал остановки...")
                break
            except Exception as e:
                logger.error(f"Ошибка в основном цикле: {e}")
                time.sleep(5)

def main():
    """Главная функция"""
    try:
        bot = SimpleTelegramBot(TELEGRAM_BOT_TOKEN)
        bot.run()
    except Exception as e:
        logger.error(f"💥 Критическая ошибка: {e}")

if __name__ == "__main__":
    main()
