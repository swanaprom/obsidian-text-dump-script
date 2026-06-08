#!/usr/bin/env bash

# ==========================================
# CONFIGURATION CONSTANTS
# ==========================================
VAULT_DIR="./SDR"
OUT_NAME="SDR_dump"

# AUTO-UPDATE INTERVAL (in seconds)
# Set to 0 to run ONLY ONCE. 
# Set to 10, 30, 60, etc., to auto-update continuously.
INTERVAL=30


# 1. Determine which Python command is available
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: Neither python3 nor python could be found on this system."
    exit 1
fi

# 2. Execution Logic
run_dump() {
    echo "[$(date '+%H:%M:%S')] Running vault dump..."
    "$PYTHON_CMD" dump.py --dir="$VAULT_DIR" --out="$OUT_NAME" "$@"
}

if [ "$INTERVAL" -eq 0 ]; then
    # Run once and exit
    run_dump "$@"
else
    # Run continuously in an infinite loop
    echo "Auto-update enabled. Dumping every $INTERVAL seconds."
    echo "Press Ctrl+C to stop."
    echo "--------------------------------------------------"
    
    while true; do
        run_dump "$@"
        sleep "$INTERVAL"
    done
fi
