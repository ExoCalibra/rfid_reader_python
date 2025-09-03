@echo off
echo ========================================
echo    RFID Reader Test Application
echo ========================================
echo.

REM Set Python path to the user's local installation
set PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python313\python.exe

REM Check if Python is installed
"%PYTHON_PATH%" --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not found at %PYTHON_PATH%
    echo Please check your Python installation
    pause
    exit /b 1
)

REM Check if pyserial is installed
"%PYTHON_PATH%" -c "import serial" >nul 2>&1
if errorlevel 1 (
    echo Installing required dependencies...
    "%PYTHON_PATH%" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo Starting RFID Reader Test...
echo.
"%PYTHON_PATH%" rfid_reader_test.py

echo.
echo Test completed. Press any key to exit...
pause >nul
