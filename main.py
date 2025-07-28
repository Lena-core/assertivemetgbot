import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from message_handler import message_handler
from config import TELEGRAM_BOT_TOKEN

# Настройка детального логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# Включаем DEBUG логи для telegram
logging.getLogger('telegram').setLevel(logging.DEBUG)
logging.getLogger('httpx').setLevel(logging.WARNING)  # Уменьшаем логи HTTP

logger = logging.getLogger(__name__)

class AssertiveMeBot:
    def __init__(self):
        self.application = None
    
    def setup_handlers(self):
        """Настройка обработчиков сообщений"""
        app = self.application
        logger.info("Настраиваем обработчики...")
        
        # Команда /start
        start_handler = CommandHandler("start", message_handler.start_command)
        app.add_handler(start_handler)
        logger.info("✅ Обработчик /start добавлен")
        
        # Обработчик пересланных сообщений
        forward_handler = MessageHandler(
            filters.FORWARDED & filters.TEXT & ~filters.COMMAND, 
            message_handler.handle_forwarded_message
        )
        app.add_handler(forward_handler)
        logger.info("✅ Обработчик пересланных сообщений добавлен")
        
        # Обработчик обратной связи (текстовые сообщения после выбора "ни один не подошел")
        text_handler = MessageHandler(
            filters.TEXT & ~filters.COMMAND & ~filters.FORWARDED,
            self._handle_text_message
        )
        app.add_handler(text_handler)
        logger.info("✅ Обработчик текстовых сообщений добавлен")
        
        # Обработчик callback кнопок
        callback_handler = CallbackQueryHandler(message_handler.handle_callback_query)
        app.add_handler(callback_handler)
        logger.info("✅ Обработчик callback кнопок добавлен")
        
        logger.info(f"✅ Всего обработчиков добавлено: {len(app.handlers[0])}")
    
    async def _handle_text_message(self, update, context):
        """Роутер для текстовых сообщений"""
        logger.info(f"📝 Получено текстовое сообщение от {update.effective_user.id}: '{update.message.text}'")
        
        # Проверяем, ждем ли мы причину отказа от пользователя
        if 'waiting_feedback_reason' in context.user_data:
            logger.info("🔄 Обрабатываем обратную связь")
            await message_handler.handle_feedback_reason(update, context)
        else:
            logger.info("🔄 Обрабатываем обычное сообщение")
            await message_handler.handle_direct_text(update, context)
    
    def run(self):
        """Запуск бота"""
        try:
            logger.info("Запуск бота Assertive.Me...")
            
            # Создаем приложение
            self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
            
            # Настраиваем обработчики
            self.setup_handlers()
            
            # Запускаем бота
            logger.info("Бот успешно запущен и готов к работе!")
            self.application.run_polling(
                allowed_updates=["message", "callback_query"],
                drop_pending_updates=True
            )
            
        except Exception as e:
            logger.error(f"Ошибка при запуске бота: {e}")
            raise

def main():
    """Главная функция"""
    try:
        bot = AssertiveMeBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки. Завершение работы...")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")

if __name__ == '__main__':
    main()
