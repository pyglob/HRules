@echo off
setlocal
set HERE=%~dp0
set VENV=%HERE%\.venv

where python >nul 2>nul || (echo Python not found & exit /b 1)

if not exist "%VENV%" (
    python -m venv "%VENV%"
)

call "%VENV%\Scripts\activate.bat"

python -m pip install --upgrade pip >nul
python -m pip install -e "%HERE%" >nul

python -m hrules.gui
endlocal
