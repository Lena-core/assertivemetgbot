#!/usr/bin/env python3
"""
Версия для python-telegram-bot 13.x (стабильная)
"""
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from config import TELEGRAM_BOT_TOKEN

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start_command(update: Update, context: CallbackContext):
    """Команда /start"""
    update.message.reply_text(
        "Привет! Я бот **Assertive.Me** и я помогу тебе переформулировать токсичные сообщения в ассертивные. Просто перешли мне любое сообщение или напиши свой текст.",
        parse_mode='Markdown'
    )

def main():
    """Запуск бота для версии 13.x"""
    try:
        logger.info("🚀 Запуск бота Assertive.Me (версия 13.x)...")
        
        # Создаем Updater
        updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
        dispatcher = updater.dispatcher
        
        # Добавляем обработчики
        dispatcher.add_handler(CommandHandler("start", start_command))
        
        # Запускаем бота
        logger.info("✅ Бот запущен успешно!")
        updater.start_polling()
        updater.idle()
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
