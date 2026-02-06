@echo off
echo ========================================
echo    DuplicateFinder - Build Executable
echo ========================================
echo.

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing PyInstaller...
    pip install pyinstaller
)

REM Check if send2trash is installed
pip show send2trash >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing send2trash...
    pip install send2trash
)

echo.
echo [INFO] Building executable...
echo.

pyinstaller --onefile --windowed --name "DuplicateFinder" --icon=NONE duplicate_finder.py

echo.
echo ========================================
if exist "dist\DuplicateFinder.exe" (
    echo [SUCCESS] Executable created at: dist\DuplicateFinder.exe
) else (
    echo [ERROR] Failed to create executable!
)
echo ========================================
echo.
pause
