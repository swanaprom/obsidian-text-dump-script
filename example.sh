#!/usr/bin/env bash

# ==========================================
# CONFIGURATION CONSTANTS
# ==========================================
# Put your target directory and output name here
VAULT_DIR="./My-Obsidian_Vault" # You can use either absolute or relative path here!
OUT_NAME="Obsidian_dump"

# ==========================================
# SCRIPT EXECUTION
# ==========================================
# 1. Determine which Python command is available
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: Neither python3 nor python could be found on this system."
    exit 1
fi

# 2. Execute the script, passing the constants as arguments
echo "Using $PYTHON_CMD to run the dump..."
"$PYTHON_CMD" dump.py --dir="$VAULT_DIR" --out="$OUT_NAME" "$@"
