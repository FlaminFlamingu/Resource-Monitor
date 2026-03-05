@echo off
setlocal
title 🔥 FlaminFlamingu Pro: Unattended Setup
color 0E

:: FILE: setup.bat
:: PURPOSE: Fully unattended environment bootstrapper.
::
:: KEY COMPONENTS:
:: 1. SMART DETECTION: Checks both the PATH and the default installation directory for Python 3.14.
:: 2. AUTO-INSTALLER: Downloads and installs Python silently only if it is missing from the system.
:: 3. LIBRARY AUTO-INSTALL: Automatically transitions to pip installations once Python is verified.
:: 4. PATH REFRESH: Uses the local file path as a fallback to ensure the script doesn't loop.

echo ======================================================
echo     FLAMINFLAMINGU RESOURCE-MONITOR SETUP
echo ======================================================
echo.

:: --- 1. SMART PYTHON CHECK ---
set "PYTHON_EXE=python"
python --version >nul 2>&1
if %errorlevel% neq 0 (
    :: Fallback: Check if it's installed in the default AppData location
    if exist "%LocalAppData%\Programs\Python\Python314\python.exe" (
        set "PYTHON_EXE=%LocalAppData%\Programs\Python\Python314\python.exe"
        echo [+] Python 3.14 detected in local folder.
    ) else (
        echo [!] Python not detected. Starting Unattended Install...
        echo [i] Downloading Python 3.14... Please wait.
        
        powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.14.0/python-3.14.0-amd64.exe' -OutFile '%TEMP%\python_installer.exe'; Start-Process '%TEMP%\python_installer.exe' -ArgumentList '/passive PrependPath=1' -Wait"
        
        :: After installation, set the path to the newly installed exe so we don't have to restart
        set "PYTHON_EXE=%LocalAppData%\Programs\Python\Python314\python.exe"
        echo [OK] Python 3.14 installed.
    )
)

:: --- 2. LIBRARY INSTALLATION (UNATTENDED) ---
echo.
echo [+] Preparing Professional Environment...
echo [1/4] Updating Pip...
"%PYTHON_EXE%" -m pip install --upgrade pip --quiet

echo [2/4] Installing Professional GUI Frameworks...
"%PYTHON_EXE%" -m pip install PySide6 pyqtgraph qt-material pillow --quiet

echo [3/4] Installing Hardware ^& Build Libraries...
"%PYTHON_EXE%" -m pip install psutil GPUtil pyadl wmi py-cpuinfo setuptools pyinstaller --quiet

echo [4/4] Verifying Project Integrity...
if not exist "assets\icon.ico" (
    echo [!] WARNING: assets\icon.ico missing.
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
set /p choice="Launch FlaminFlamingu Monitor now? (y/n): "
if /i "%choice%"=="y" (
    echo Launching...
    "%PYTHON_EXE%" main.py
) else (
    echo.
    echo To build your .exe later, use:
    echo "%PYTHON_EXE%" -m PyInstaller --onefile --windowed --icon="assets/icon.ico" main.py
    pause
)