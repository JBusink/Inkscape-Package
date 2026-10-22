@echo off
setlocal
set "installer=%~dp0Maintenance\install.ps1"
if not exist "%installer%" set "installer=%~dp0Modular packages\Science-symbols\Maintenance\install.ps1"
if not exist "%installer%" (
    echo Installer files are missing. Extract the complete ZIP before running Install.cmd.
    pause
    exit /b 1
)
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%installer%"
set "install_result=%errorlevel%"
if not "%install_result%"=="0" echo Installation failed. Read the message above before trying again.
pause
exit /b %install_result%
