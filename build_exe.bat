@echo off
echo ========================================
echo    DuplicateFinder - Build Executavel
echo ========================================
echo.

REM Verificar se PyInstaller esta instalado
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [INFO] Instalando PyInstaller...
    pip install pyinstaller
)

REM Verificar se send2trash esta instalado
pip show send2trash >nul 2>&1
if errorlevel 1 (
    echo [INFO] Instalando send2trash...
    pip install send2trash
)

echo.
echo [INFO] Gerando executavel...
echo.

pyinstaller --onefile --windowed --name "DuplicateFinder" --icon=NONE duplicate_finder.py

echo.
echo ========================================
if exist "dist\DuplicateFinder.exe" (
    echo [SUCESSO] Executavel criado em: dist\DuplicateFinder.exe
) else (
    echo [ERRO] Falha ao criar executavel!
)
echo ========================================
echo.
pause
