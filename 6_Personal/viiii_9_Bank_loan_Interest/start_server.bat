@echo off
:: Set paths
set VENV_PATH=D:\2025\venv\Scripts
set PROJECT_PATH=D:\2025\6_Personal\viiii_9_Bank_loan_Interest

:: Activate the virtual environment
call %VENV_PATH%\activate.bat

:: Change to the project directory
cd /d %PROJECT_PATH%

:: Start the HTTP server
python -m http.server 8080 --bind 0.0.0.0