#!/bin/bash
echo "Переустановка зависимостей..."
echo

echo "Удаление старых пакетов..."
pip uninstall -y python-telegram-bot openai python-dotenv

echo
echo "Установка новых версий..."
pip install python-telegram-bot==20.8
pip install openai==1.35.0
pip install python-dotenv==1.0.0

echo
echo "Готово! Теперь можно запускать бота:"
echo "python main.py"
