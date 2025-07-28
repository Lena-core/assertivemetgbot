#!/usr/bin/env python3
"""
Полная версия Assertive.Me бота для python-telegram-bot 13.x
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

from config import TELEGRAM_BOT_TOKEN, MESSAGES
from validators import validator
from llm_service_v13 import llm_service_v13
from database import db_manager

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class MessageHandlerV13:
    def __init__(self):
        self.processing_messages = {}
        self.user_requests = {}
    
    def start_command(self, update: Update, context: CallbackContext):
        """Обработчик команды /start"""
        user_id = update.effective_user.id
        logger.info(f"🚀 Пользователь {user_id} выполнил команду /start")
        
        try:
            update.message.reply_text(
                MESSAGES['welcome'],
                parse_mode='Markdown'
            )
            logger.info(f"✅ Отправлено приветственное сообщение пользователю {user_id}")
        except Exception as e:
            logger.error(f"❌ Ошибка отправки приветствия пользователю {user_id}: {e}")
    
    def handle_forwarded_message(self, update: Update, context: CallbackContext):
        """Обработчик пересланных сообщений"""
        message = update.message
        user_id = update.effective_user.id
        logger.info(f"🔄 Пользователь {user_id} переслал сообщение")
        
        if not message.text:
            logger.warning(f"⚠️ Пользователь {user_id} переслал нетекстовое сообщение")
            message.reply_text("Я могу работать только с текстовыми сообщениями.")
            return
        
        # Получаем информацию об источнике пересылки
        forward_from_chat = message.forward_from_chat
        source_chat_id = forward_from_chat.id if forward_from_chat else None
        source_chat_type = forward_from_chat.type if forward_from_chat else None
        source_chat_title = forward_from_chat.title if forward_from_chat else None
        
        logger.info(f"📝 Текст пересланного сообщения (длина {len(message.text)}): '{message.text[:100]}{'...' if len(message.text) > 100 else ''}'")
        
        self._process_message(
            update, context, message.text,
            message_type='forwarded_message',
            source_chat_id=source_chat_id,
            source_chat_type=source_chat_type,
            source_chat_title=source_chat_title
        )
    
    def handle_direct_text(self, update: Update, context: CallbackContext):
        """Обработчик прямого ввода текста"""
        message = update.message
        user_id = update.effective_user.id
        
        # Проверяем, ждем ли мы причину отказа
        if context.user_data.get('waiting_feedback_reason'):
            logger.info("🔄 Обрабатываем обратную связь")
            self.handle_feedback_reason(update, context)
            return
        
        logger.info(f"✍️ Пользователь {user_id} написал сообщение: '{message.text[:50]}{'...' if len(message.text) > 50 else ''}'")
        
        # Проверяем, что это не команда
        if message.text.startswith('/'):
            logger.info(f"⚠️ Пользователь {user_id} отправил команду - игнорируем")
            return
        
        self._process_message(
            update, context, message.text,
            message_type='direct_text'
        )
    
    def _process_message(self, update: Update, context: CallbackContext, 
                        text: str, message_type: str, source_chat_id=None, 
                        source_chat_type=None, source_chat_title=None):
        """Основная логика обработки сообщения"""
        user_id = update.effective_user.id
        
        # Отправляем сообщение о обработке
        try:
            processing_msg = update.message.reply_text(MESSAGES['processing'])
            self.processing_messages[user_id] = processing_msg.message_id
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения об обработке: {e}")
        
        # Очищаем и валидируем текст
        clean_text = validator.clean_text(text)
        is_valid, validation_error = validator.is_valid_for_processing(clean_text)
        
        if not is_valid:
            self._handle_validation_error(update, context, validation_error)
            return
        
        try:
            # Генерируем варианты через LLM
            variants = llm_service_v13.generate_assertive_variants(clean_text)
            
            if not variants:
                self._send_error_message(update, context)
                return
            
            # Сохраняем запрос в базу данных
            request_id = db_manager.save_request(
                user_id=user_id,
                message_type=message_type,
                request_text=clean_text,
                response_variants=variants,
                source_chat_id=source_chat_id,
                source_chat_type=source_chat_type,
                source_chat_title=source_chat_title
            )
            
            # Сохраняем связь пользователя с запросом
            self.user_requests[user_id] = request_id
            
            # Удаляем сообщение "обрабатывается"
            try:
                context.bot.delete_message(
                    chat_id=update.effective_chat.id,
                    message_id=self.processing_messages[user_id]
                )
            except:
                pass
            
            # Отправляем варианты с кнопками
            self._send_variants_with_buttons(update, context, variants)
            
        except Exception as e:
            logger.error(f"Ошибка при обработке сообщения: {e}")
            self._send_error_message(update, context)
    
    def _handle_validation_error(self, update: Update, context: CallbackContext, error_type: str):
        """Обработка ошибок валидации"""
        user_id = update.effective_user.id
        
        # Удаляем сообщение "обрабатывается"
        try:
            context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=self.processing_messages[user_id]
            )
        except:
            pass
        
        if error_type == "too_long":
            update.message.reply_text(MESSAGES['too_long'])
        elif error_type in ["too_short", "not_toxic"]:
            update.message.reply_text(MESSAGES['too_short_or_non_toxic'])
    
    def _send_error_message(self, update: Update, context: CallbackContext):
        """Отправка сообщения об ошибке"""
        user_id = update.effective_user.id
        
        # Удаляем сообщение "обрабатывается"
        try:
            context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=self.processing_messages[user_id]
            )
        except:
            pass
        
        update.message.reply_text(MESSAGES['error'])
    
    def _send_variants_with_buttons(self, update: Update, context: CallbackContext, variants: list):
        """Отправка вариантов с кнопками обратной связи"""
        # Форматируем сообщение с вариантами
        message_text = llm_service_v13.format_variants_message(variants)
        
        # Создаем inline кнопки
        keyboard = []
        for i in range(len(variants)):
            keyboard.append([InlineKeyboardButton(f"Выбрать {i+1}", callback_data=f"select_{i+1}")])
        
        keyboard.append([InlineKeyboardButton("Ни один не подошел", callback_data="select_none")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text(
            message_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    def handle_callback_query(self, update: Update, context: CallbackContext):
        """Обработчик нажатий на inline кнопки"""
        query = update.callback_query
        user_id = update.effective_user.id
        
        query.answer()  # Подтверждаем получение callback
        
        # Получаем ID запроса пользователя
        request_id = self.user_requests.get(user_id)
        if not request_id:
            query.edit_message_text("Ошибка: запрос не найден.")
            return
        
        callback_data = query.data
        
        if callback_data.startswith("select_"):
            if callback_data == "select_none":
                # Пользователь выбрал "Ни один не подошел"
                query.edit_message_text(
                    query.message.text + "\n\n" + MESSAGES['feedback_request']
                )
                # Устанавливаем флаг ожидания причины
                context.user_data['waiting_feedback_reason'] = request_id
            else:
                # Пользователь выбрал один из вариантов
                variant_index = int(callback_data.split("_")[1])
                
                # Сохраняем выбор в базу данных
                db_manager.save_feedback(request_id, selected_variant_index=variant_index)
                
                query.edit_message_text(
                    query.message.text + f"\n\n✅ Вы выбрали вариант {variant_index}. " + MESSAGES['feedback_thanks']
                )
                
                # Удаляем связь
                if user_id in self.user_requests:
                    del self.user_requests[user_id]
    
    def handle_feedback_reason(self, update: Update, context: CallbackContext):
        """Обработчик причины отказа от всех вариантов"""
        request_id = context.user_data.get('waiting_feedback_reason')
        if not request_id:
            return
        
        feedback_reason = update.message.text
        
        # Сохраняем причину в базу данных
        db_manager.save_feedback(request_id, feedback_reason=feedback_reason)
        
        update.message.reply_text(MESSAGES['feedback_thanks'])
        
        # Очищаем данные
        del context.user_data['waiting_feedback_reason']
        user_id = update.effective_user.id
        if user_id in self.user_requests:
            del self.user_requests[user_id]


def main():
    """Главная функция запуска бота"""
    try:
        logger.info("🚀 Запуск бота Assertive.Me (версия 13.x)...")
        
        # Создаем Updater
        updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
        dispatcher = updater.dispatcher
        
        # Создаем обработчик сообщений
        message_handler = MessageHandlerV13()
        
        # Добавляем обработчики
        logger.info("➕ Добавляем обработчики...")
        
        # Команда /start
        dispatcher.add_handler(CommandHandler("start", message_handler.start_command))
        logger.info("✅ Обработчик /start добавлен")
        
        # Обработчик пересланных сообщений
        dispatcher.add_handler(MessageHandler(
            Filters.forwarded & Filters.text & ~Filters.command,
            message_handler.handle_forwarded_message
        ))
        logger.info("✅ Обработчик пересланных сообщений добавлен")
        
        # Обработчик прямого текста
        dispatcher.add_handler(MessageHandler(
            Filters.text & ~Filters.command & ~Filters.forwarded,
            message_handler.handle_direct_text
        ))
        logger.info("✅ Обработчик текста добавлен")
        
        # Обработчик кнопок
        dispatcher.add_handler(CallbackQueryHandler(message_handler.handle_callback_query))
        logger.info("✅ Обработчик кнопок добавлен")
        
        # Запускаем бота
        logger.info("🎯 Бот успешно запущен и готов к работе!")
        updater.start_polling()
        updater.idle()
        
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("👋 Получен сигнал остановки. Завершение работы...")
    except Exception as e:
        logger.error(f"💥 Неожиданная ошибка: {e}")
