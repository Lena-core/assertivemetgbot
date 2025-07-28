from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
import asyncio
import logging

from config import MESSAGES
from validators import validator
from llm_service import llm_service
from database import db_manager

# Логгер для обработчика сообщений
logger = logging.getLogger(__name__)

class MessageHandler:
    def __init__(self):
        self.processing_messages = {}  # Для отслеживания сообщений "обрабатывается"
        self.user_requests = {}  # Для связи пользователей с их запросами
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user_id = update.effective_user.id
        logger.info(f"🚀 Пользователь {user_id} выполнил команду /start")
        
        try:
            await update.message.reply_text(
                MESSAGES['welcome'],
                parse_mode='Markdown'
            )
            logger.info(f"✅ Отправлено приветственное сообщение пользователю {user_id}")
        except Exception as e:
            logger.error(f"❌ Ошибка отправки приветствия пользователю {user_id}: {e}")
    
    async def handle_forwarded_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик пересланных сообщений"""
        message = update.message
        user_id = update.effective_user.id
        logger.info(f"🔄 Пользователь {user_id} переслал сообщение")
        
        if not message.text:
            logger.warning(f"⚠️ Пользователь {user_id} переслал нетекстовое сообщение")
            await message.reply_text("Я могу работать только с текстовыми сообщениями.")
            return
        
        # Получаем информацию об источнике пересылки
        forward_from_chat = message.forward_from_chat
        source_chat_id = forward_from_chat.id if forward_from_chat else None
        source_chat_type = forward_from_chat.type if forward_from_chat else None
        source_chat_title = forward_from_chat.title if forward_from_chat else None
        
        logger.info(f"📝 Текст пересланного сообщения (длина {len(message.text)}): '{message.text[:100]}{'...' if len(message.text) > 100 else ''}'")
        
        await self._process_message(
            update, context, message.text, 
            message_type='forwarded_message',
            source_chat_id=source_chat_id,
            source_chat_type=source_chat_type,
            source_chat_title=source_chat_title
        )
    
    async def handle_direct_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик прямого ввода текста"""
        message = update.message
        
        # Проверяем, что это не команда
        if message.text.startswith('/'):
            return
        
        await self._process_message(
            update, context, message.text,
            message_type='direct_text'
        )
    
    async def _process_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                             text: str, message_type: str, source_chat_id=None, 
                             source_chat_type=None, source_chat_title=None):
        """Основная логика обработки сообщения"""
        user_id = update.effective_user.id
        
        # Показываем индикатор "печатает"
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action=ChatAction.TYPING
        )
        
        # Отправляем сообщение о обработке
        processing_msg = await update.message.reply_text(MESSAGES['processing'])
        self.processing_messages[user_id] = processing_msg.message_id
        
        # Очищаем и валидируем текст
        clean_text = validator.clean_text(text)
        is_valid, validation_error = validator.is_valid_for_processing(clean_text)
        
        if not is_valid:
            await self._handle_validation_error(update, context, validation_error)
            return
        
        try:
            # Генерируем варианты через LLM
            variants = llm_service.generate_assertive_variants(clean_text)
            
            if not variants:
                await self._send_error_message(update, context)
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
            
            # Сохраняем связь пользователя с запросом для обратной связи
            self.user_requests[user_id] = request_id
            
            # Удаляем сообщение "обрабатывается"
            try:
                await context.bot.delete_message(
                    chat_id=update.effective_chat.id,
                    message_id=self.processing_messages[user_id]
                )
            except:
                pass  # Игнорируем ошибки удаления
            
            # Отправляем варианты с кнопками
            await self._send_variants_with_buttons(update, context, variants)
            
        except Exception as e:
            print(f"Ошибка при обработке сообщения: {e}")
            await self._send_error_message(update, context)
    
    async def _handle_validation_error(self, update: Update, context: ContextTypes.DEFAULT_TYPE, error_type: str):
        """Обработка ошибок валидации"""
        user_id = update.effective_user.id
        
        # Удаляем сообщение "обрабатывается"
        try:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=self.processing_messages[user_id]
            )
        except:
            pass
        
        if error_type == "too_long":
            await update.message.reply_text(MESSAGES['too_long'])
        elif error_type in ["too_short", "not_toxic"]:
            await update.message.reply_text(MESSAGES['too_short_or_non_toxic'])
    
    async def _send_error_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Отправка сообщения об ошибке"""
        user_id = update.effective_user.id
        
        # Удаляем сообщение "обрабатывается"
        try:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=self.processing_messages[user_id]
            )
        except:
            pass
        
        await update.message.reply_text(MESSAGES['error'])
    
    async def _send_variants_with_buttons(self, update: Update, context: ContextTypes.DEFAULT_TYPE, variants: list):
        """Отправка вариантов с кнопками обратной связи"""
        # Форматируем сообщение с вариантами
        message_text = llm_service.format_variants_message(variants)
        
        # Создаем inline кнопки
        keyboard = []
        for i in range(len(variants)):
            keyboard.append([InlineKeyboardButton(f"Выбрать {i+1}", callback_data=f"select_{i+1}")])
        
        keyboard.append([InlineKeyboardButton("Ни один не подошел", callback_data="select_none")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            message_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на inline кнопки"""
        query = update.callback_query
        user_id = update.effective_user.id
        
        await query.answer()  # Подтверждаем получение callback
        
        # Получаем ID запроса пользователя
        request_id = self.user_requests.get(user_id)
        if not request_id:
            await query.edit_message_text("Ошибка: запрос не найден.")
            return
        
        callback_data = query.data
        
        if callback_data.startswith("select_"):
            if callback_data == "select_none":
                # Пользователь выбрал "Ни один не подошел"
                await query.edit_message_text(
                    query.message.text + "\n\n" + MESSAGES['feedback_request']
                )
                # Устанавливаем флаг ожидания причины
                context.user_data['waiting_feedback_reason'] = request_id
            else:
                # Пользователь выбрал один из вариантов
                variant_index = int(callback_data.split("_")[1])
                
                # Сохраняем выбор в базу данных
                db_manager.save_feedback(request_id, selected_variant_index=variant_index)
                
                await query.edit_message_text(
                    query.message.text + f"\n\n✅ Вы выбрали вариант {variant_index}. " + MESSAGES['feedback_thanks']
                )
                
                # Удаляем связь
                if user_id in self.user_requests:
                    del self.user_requests[user_id]
    
    async def handle_feedback_reason(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик причины отказа от всех вариантов"""
        if 'waiting_feedback_reason' not in context.user_data:
            return
        
        request_id = context.user_data['waiting_feedback_reason']
        feedback_reason = update.message.text
        
        # Сохраняем причину в базу данных
        db_manager.save_feedback(request_id, feedback_reason=feedback_reason)
        
        await update.message.reply_text(MESSAGES['feedback_thanks'])
        
        # Очищаем данные
        del context.user_data['waiting_feedback_reason']
        user_id = update.effective_user.id
        if user_id in self.user_requests:
            del self.user_requests[user_id]

# Глобальный экземпляр обработчика
message_handler = MessageHandler()
