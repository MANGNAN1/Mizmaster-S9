@echo off
REM Convert JPG and PNG to GIF

REM Ensure Python is available
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python and try again.
    exit /b 1
)

REM Run the Python script with all dragged files
python convert_images.py %*

pause
