@echo off
echo 🔧 SWITCHING TO ULTRA-SOFT VALIDATOR
echo ========================================
echo.

cd /d C:\Projects\\assertiveme\\assertive-me-bot

echo 📁 Creating a backup of the current validator...
copy validators.py validators_backup.py >nul

echo 🔄 Switching to ultra-soft validator...
copy validators_ultra_soft.py validators.py >nul

echo ✅ Done! Now the bot will allow almost ALL messages.

echo.
echo 💡 Only the following will be rejected:
echo    - Empty messages
echo    - Only punctuation marks
echo    - Only numbers
echo    - Too short (less than 10 characters)
echo    - Too long (more than 4000 characters)

echo.
echo 🚀 Restart the bot:
echo python main_simple_stable.py

echo.
echo 🔙 To restore the regular validator:
echo copy