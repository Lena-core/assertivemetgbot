@echo off
echo 🔧 УСТАНОВКА СТАБИЛЬНОЙ ВЕРСИИ (13.x)
echo ===================================
echo.

cd /d C:\Projects\assertive-me-bot
echo 📂 Переходим в папку проекта...

echo.
echo 🗑️ Удаляем проблемную версию 20.x...
call venv\Scripts\activate
pip uninstall -y python-telegram-bot openai

echo.
echo 📦 Устанавливаем стабильную версию 13.x...
pip install --upgrade pip
pip install python-telegram-bot==13.15
pip install openai==0.28.1
pip install python-dotenv==1.0.0
pip install requests==2.31.0

echo.
echo ✅ Проверяем установку...
python -c "import telegram; print('✅ Telegram:', telegram.__version__)"
python -c "import openai; print('✅ OpenAI:', openai.version.VERSION)"

echo.
echo 🥳 ГОТОВО! Теперь можете запускать:
echo python main_v13_full.py
echo.
pause
