@echo off
title 🔥 FlaminFlamingu Pro: Developer Setup
color 0E
echo ======================================================
echo    FLAMINFLAMINGU RESOURCE-MONITOR : PRO SETUP
echo ======================================================
echo.

:: 1. Check Python Installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.12+ from python.org.
    pause
    exit /b
)

echo [+] Python Detected.
echo [1/4] Updating Pip...
python -m pip install --upgrade pip --quiet

echo [2/4] Installing Professional GUI Frameworks...
:: PySide6 = Pro Windows UI, PyQtGraph = 60FPS Hardware Charts
:: Qt-Material = Modern Dark Mode, Pillow = Image Handling
python -m pip install PySide6 pyqtgraph qt-material pillow --quiet

echo [3/4] Installing Hardware & Build Libraries...
python -m pip install psutil GPUtil pyadl wmi py-cpuinfo setuptools pyinstaller --quiet

echo [4/4] Verifying Project Integrity...
if not exist "assets\icon.ico" (
    echo [!] WARNING: assets\icon.ico missing. Using default icon for build.
)
if exist "build" (
    echo [i] Cleaning old build cache...
    rd /s /q build
)

echo.
echo ======================================================
echo ✅ SETUP COMPLETE: PRO ENVIRONMENT IS READY
echo ======================================================
echo.
echo [INFO] You can now build the Pro GUI or run the TUI.
echo.
set /p choice="Launch FlaminFlamingu Monitor now? (y/n): "
if /i "%choice%"=="y" (
    echo Launching...
    python main.py
) else (
    echo.
    echo To build your .exe later, use:
    echo python -m PyInstaller --onefile --windowed --icon="assets/icon.ico" main.py
    pause
)