@echo off
cd /d "%~dp0"
echo Installing libraries...
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo Python was not found. Install it from python.org and tick "Add Python to PATH", then run this again.
  pause
  exit /b 1
)
echo.
echo === Step 1: collecting submissions ===
python 01_collect.py || goto :error
echo.
echo === Step 9: census list, PDFs and texts (about 5 minutes) ===
python 09_census.py || goto :error
echo.
echo === Step 6: scoring positions ===
python 06_analyse.py || goto :error
echo.
echo === Step 7: building the page ===
python 07_build_page.py || goto :error
echo.
echo All done. Open docs\index.html to see the tracker.
pause
exit /b 0

:error
echo.
echo Something went wrong above. Copy the error message and send it to Claude.
pause
exit /b 1
