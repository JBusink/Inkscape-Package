@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  python "Maintenance\build.py"
) else (
  py -3 "Maintenance\build.py"
)
if errorlevel 1 pause
