@echo off@echo off

echo ==========================================echo =========================================

echo   Secure Data Sharing System - QUICK RUNecho   Secure Data Sharing System - QUICK

echo ==========================================echo =========================================

echo.echo.

echo Quick startup without tests...echo Starting web application without tests...

echo.echo.

cd /d "C:\Users\gunda\Secure_Data_Sharing-System"cd /d "C:\Users\gunda\Secure_Data_Sharing-System"



echo Starting web server...echo Open your browser and go to: http://localhost:5000

echo Open your browser: http://localhost:5000echo.

echo.echo Features Available:

echo - Message encryption/decryption

python app_simple.pyecho - File encryption/decryption  
echo - User management
echo - Activity logging
echo - REST API endpoints
echo.
echo Press Ctrl+C to stop the server
echo.

python app_simple.py
