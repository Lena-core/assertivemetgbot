@echo off
echo 🔧 РЕШЕНИЕ ПРОБЛЕМЫ Python 3.13 + imghdr
echo =====================================
echo.

cd /d C:\Projects\assertive-me-bot
call venv\Scripts\activate

echo 📝 Создаем заглушку для imghdr...
python -c "
import os
site_packages = os.path.join('venv', 'Lib', 'site-packages', 'imghdr.py')
with open(site_packages, 'w') as f:
    f.write('''
def what(file, h=None):
    if hasattr(file, \"name\"):
        filename = file.name.lower()
        if filename.endswith((\".jpg\", \".jpeg\")):
            return \"jpeg\"
        elif filename.endswith(\".png\"):
            return \"png\"
        elif filename.endswith(\".gif\"):
            return \"gif\"
        elif filename.endswith(\".bmp\"):
            return \"bmp\"
        elif filename.endswith(\".webp\"):
            return \"webp\"
    return None

tests = []
''')
print('✅ Заглушка создана')
"

echo.
echo 🧪 Проверяем telegram...
python -c "import telegram; print('✅ Telegram:', telegram.__version__)"

if errorlevel 1 (
    echo ❌ Все еще ошибка. Попробуйте альтернативное решение.
) else (
    echo ✅ Проблема решена!
    echo.
    echo 🚀 Теперь можете запускать:
    echo python main_v13_full.py
)

pause
