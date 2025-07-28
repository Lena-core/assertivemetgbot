@echo off
echo 🚀 УСТАНОВКА ПРОСТОЙ СТАБИЛЬНОЙ ВЕРСИИ
echo ====================================
echo.

cd /d C:\Projects\assertive-me-bot
echo 📂 Переходим в папку проекта...

echo.
echo 🗑️ Удаляем проблемные библиотеки...
call venv\Scripts\activate
pip uninstall -y python-telegram-bot APScheduler tornado

echo.
echo 📦 Устанавливаем только необходимые библиотеки...
pip install --upgrade pip
pip install requests==2.31.0
pip install openai==0.28.1
pip install python-dotenv==1.0.0

echo.
echo ✅ Проверяем установку...
python -c "import requests; print('✅ requests:', requests.__version__)"
python -c "import openai; print('✅ OpenAI:', openai.version.VERSION)"
python -c "import dotenv; print('✅ dotenv работает')"

echo.
echo 🥳 ГОТОВО! Теперь можете запускать:
echo python main_simple_stable.py
echo.
pause
