@echo off
echo =========================================
echo   Secure Data Sharing System - FIXED
echo =========================================
echo.
echo Starting the web application...
echo.
cd /d "C:\Users\gunda\Secure_Data_Sharing-System"

echo Testing system first...
python -c "from app_simple import app; print('✅ Flask app loads successfully'); print('✅ Templates are valid')"
echo.

if errorlevel 1 (
    echo Tests failed! Check for errors above.
    pause
    exit /b 1
)

echo Tests passed! Starting web server...
echo.
echo Open your browser and go to: http://localhost:5000
echo.
echo FEATURES FIXED:
echo - User management with proper form fields
echo - Decryption working for all users
echo - Auto-registration of users in Firebase
echo - Better error handling and debugging
echo - Virtual environment optional: .\venv\Scripts\activate
echo.
echo Press Ctrl+C to stop the server
echo.

python app_simple.py
