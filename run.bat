@echo off
title Assertive.Me Bot Launcher
echo.
echo 🤖 ASSERTIVE.ME BOT LAUNCHER
echo ============================
echo.

echo Активация виртуальной среды...
call venv\Scripts\activate

echo.
echo Проверка компонентов...
python test.py

echo.
set /p choice="Продолжить запуск бота? (y/n): "
if /i "%choice%"=="y" (
    echo.
    echo 🚀 Запуск бота...
    python main.py
) else (
    echo Отменено пользователем.
    pause
)
