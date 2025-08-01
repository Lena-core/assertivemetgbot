import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from message_handler import message_handler
from config import TELEGRAM_BOT_TOKEN

# Настройка детального логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Упрощенная версия запуска бота"""
    try:
        logger.info("🚀 Запуск бота Assertive.Me (упрощенная версия)...")
        
        # Создаем приложение
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        # Добавляем обработчики
        logger.info("➕ Добавляем обработчики...")
        
        # Команда /start
        application.add_handler(CommandHandler("start", message_handler.start_command))
        logger.info("✅ Обработчик /start добавлен")
        
        # Обработчик пересланных сообщений
        application.add_handler(MessageHandler(
            filters.FORWARDED & filters.TEXT & ~filters.COMMAND, 
            message_handler.handle_forwarded_message
        ))
        logger.info("✅ Обработчик пересланных сообщений добавлен")
        
        # Обработчик прямого текста
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND & ~filters.FORWARDED,
            message_handler.handle_direct_text
        ))
        logger.info("✅ Обработчик текста добавлен")
        
        # Обработчик кнопок
        application.add_handler(CallbackQueryHandler(message_handler.handle_callback_query))
        logger.info("✅ Обработчик кнопок добавлен")
        
        # Запускаем бота
        logger.info("🎯 Запуск polling...")
        application.run_polling(
            allowed_updates=["message", "callback_query"],
            drop_pending_updates=True
        )
        
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("👋 Получен сигнал остановки. Завершение работы...")
    except Exception as e:
        logger.error(f"💥 Неожиданная ошибка: {e}")
