@echo off
REM ═══════════════════════════════════════════════════════════════════════════════
REM Script de compilation: generate_secret.py → EXE (PyInstaller)
REM ═══════════════════════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo COMPILATION EXECUTABLE - Shamir Generate Secret
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

REM Vérifie que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERREUR: Python n'est pas trouvé dans PATH
    echo    Installez Python ou ajoutez-le au PATH Windows
    echo    https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python trouvé

REM Vérifie PyInstaller
echo.
echo Installation de PyInstaller (si nécessaire)...
pip install pyinstaller --quiet
if errorlevel 1 (
    echo ❌ ERREUR: Impossible d'installer PyInstaller
    pause
    exit /b 1
)

echo ✅ PyInstaller prêt

REM Compile l'EXE
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo COMPILATION EN COURS...
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

cd /d "%~dp0"

pyinstaller ^
    --onefile ^
    --name "Shamir_Generate" ^
    --icon=NONE ^
    --add-data "core\mots.py:core" ^
    --add-data "core\shamir_polynomial_robust.py:core" ^
    core\generate_secret.py

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo COMPILATION TERMINÉE
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

if exist "dist\Shamir_Generate.exe" (
    echo ✅ EXE créé avec succès!
    echo.
    echo 📍 Localisation: %cd%\dist\Shamir_Generate.exe
    echo.
    echo 📋 Instructions:
    echo    1. Double-clic sur Shamir_Generate.exe
    echo    2. Génère 24 mots et 3 PARTS Shamir
    echo    3. Stocke shamir_metadata.json automatiquement
    echo.
    echo Fichiers générés:
    dir /b "dist\"
) else (
    echo ❌ ERREUR: L'EXE n'a pas été créé
)

echo.
pause
