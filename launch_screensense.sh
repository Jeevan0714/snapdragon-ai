#!/usr/bin/env bash
# ==============================================================================
# ScreenSense Guardian Launcher
# Launches the floating desktop pill widget without needing a terminal window.
# ==============================================================================

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CD_PATH="$SCRIPT_DIR"

cd "$CD_PATH"

if [ -f ".venv/bin/python" ]; then
    PYTHON_EXEC=".venv/bin/python"
else
    PYTHON_EXEC="python3"
fi

echo "[ScreenSense] Starting ScreenSense Guardian Floating Widget..."
exec "$PYTHON_EXEC" -m screensense.app --widget "$@"
