@echo off
cd /d "%~dp0"
echo Downloading and extracting every submission (about 5 minutes)...
python 09_census.py
echo.
echo Done. You can close this window.
pause
