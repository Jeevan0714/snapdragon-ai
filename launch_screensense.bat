@echo off
REM ==============================================================================
REM ScreenSense Guardian Windows Launcher
REM Double-click this file to launch the floating desktop widget on Windows.
REM ==============================================================================

cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    start "" ".venv\Scripts\pythonw.exe" -m screensense.app --widget
) else (
    start "" pythonw -m screensense.app --widget
)
