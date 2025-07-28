#!/usr/bin/env python3
"""
Минимальный тест Telegram бота для поиска ошибки
"""
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import TELEGRAM_BOT_TOKEN

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Простая команда /start"""
    await update.message.reply_text("🤖 Привет! Бот работает!")
    logger.info(f"Отправлен ответ пользователю {update.effective_user.id}")

def main():
    """Минимальный запуск бота"""
    try:
        logger.info("🧪 МИНИМАЛЬНЫЙ ТЕСТ БОТА")
        logger.info("=" * 30)
        
        # Проверяем токен
        logger.info(f"🔑 Токен: {TELEGRAM_BOT_TOKEN[:10]}...")
        
        # Создаем приложение
        logger.info("📱 Создаем Application...")
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        logger.info("✅ Application создан успешно")
        
        # Добавляем один обработчик
        logger.info("➕ Добавляем обработчик /start...")
        application.add_handler(CommandHandler("start", start_command))
        logger.info("✅ Обработчик добавлен")
        
        # ВАЖНО: Проверяем, что приложение готово
        logger.info("🔍 Проверяем состояние приложения...")
        logger.info(f"   Обработчиков: {len(application.handlers)}")
        
        # Запускаем polling
        logger.info("🚀 Запускаем polling...")
        application.run_polling()
        
    except Exception as e:
        logger.error(f"❌ ОШИБКА: {e}")
        import traceback
        logger.error("📜 Полный traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("👋 Остановка по Ctrl+C")
    except Exception as e:
        logger.error(f"💥 Критическая ошибка: {e}")
