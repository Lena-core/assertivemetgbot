@echo off
echo 🔧 ПОЛНАЯ ПЕРЕУСТАНОВКА ОКРУЖЕНИЯ
echo =====================================
echo.

cd /d C:\Projects\assertive-me-bot
echo 📂 Переходим в папку проекта...

echo.
echo 🗑️ Удаляем старую виртуальную среду...
if exist venv rmdir /s /q venv

echo.
echo 🆕 Создаем новую виртуальную среду...
python -m venv venv

echo.
echo ⚡ Активируем виртуальную среду...
call venv\Scripts\activate

echo.
echo 📦 Устанавливаем зависимости...
pip install --upgrade pip
pip install python-telegram-bot==20.8
pip install openai==1.35.0
pip install python-dotenv==1.0.0

echo.
echo ✅ Проверяем установку...
python -c "import telegram; print('Telegram:', telegram.__version__)"
python -c "import openai; print('OpenAI:', openai.__version__)"

echo.
echo 🎉 ГОТОВО! Теперь можете запускать:
echo python main.py
pause
