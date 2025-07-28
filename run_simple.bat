@echo off
title Assertive.Me Bot Simple Stable Launcher
echo.
echo 🤖 ASSERTIVE.ME BOT SIMPLE LAUNCHER
echo ===================================
echo.

cd /d C:\Projects\assertive-me-bot

echo Активация виртуальной среды...
call venv\Scripts\activate

echo.
echo 🔍 Проверка библиотек...
python -c "import requests, openai, dotenv; print('✅ Все библиотеки на месте')" 2>nul
if errorlevel 1 (
    echo ❌ Библиотеки не установлены!
    echo 💡 Запустите install_simple.bat для установки
    pause
    exit /b 1
)

echo.
echo ✅ Все библиотеки установлены правильно!
echo.
set /p choice="Запустить простую стабильную версию бота? (y/n): "
if /i "%choice%"=="y" (
    echo.
    echo 🚀 Запуск простой стабильной версии...
    python main_simple_stable.py
) else (
    echo Отменено пользователем.
    pause
)
