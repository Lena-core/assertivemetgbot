@echo off
title Assertive.Me Bot v13.x Launcher
echo.
echo 🤖 ASSERTIVE.ME BOT LAUNCHER (v13.x)
echo ========================================
echo.

cd /d C:\Projects\assertive-me-bot

echo Активация виртуальной среды...
call venv\Scripts\activate

echo.
echo 🔍 Проверка версий...
python -c "import telegram; print('Telegram:', telegram.__version__)" 2>nul
if errorlevel 1 (
    echo ❌ Telegram бот библиотека не установлена!
    echo 💡 Запустите install_v13.bat для установки
    pause
    exit /b 1
)

python -c "import openai; print('OpenAI:', openai.version.VERSION)" 2>nul
if errorlevel 1 (
    echo ❌ OpenAI библиотека не установлена!
    echo 💡 Запустите install_v13.bat для установки
    pause
    exit /b 1
)

echo.
echo ✅ Все библиотеки установлены правильно!
echo.
set /p choice="Запустить бота? (y/n): "
if /i "%choice%"=="y" (
    echo.
    echo 🚀 Запуск бота версии 13.x...
    python main_v13_full.py
) else (
    echo Отменено пользователем.
    pause
)
