#!/bin/bash

echo "[ WORKER ] Building Release"
USERNAME=$(whoami)
SOURCE_FILE="./main.bin"
RENAMED_FILE="./deoryz_wallet_searcher_latest_linux64.bin"
PYTHON_SCRIPT="./main.py"



# Check if main.bin exists, if not, build it using Nuitka
if [ ! -f "$SOURCE_FILE" ]; then
    echo "[ BUILDER ] main.bin not found, building with Nuitka..."
    nuitka --onefile --follow-imports --lto=yes --remove-output --include-package=xrpl --include-package=Crypto --include-package=coincurve --include-package=eth_hash --include-data-dir="./venv/lib/python3.11/site-packages/xrpl/core/binarycodec/definitions=xrpl/core/binarycodec/definitions/" --include-data-dir="venv/lib/python3.11/site-packages/bip_utils/bip/bip39/wordlist=bip_utils/bip/bip39/wordlist" --jobs=8 "$PYTHON_SCRIPT"
    
    # Check if build was successful
    if [ ! -f "$SOURCE_FILE" ]; then
        echo "[ ERROR ] Failed to build main.bin!"
        exit 1
    fi
fi

# Rename main.bin to deoryz_wallet_searcher_latest_linux64.bin
echo "[ WORKER ] Renaming main.bin to deoryz_wallet_searcher_latest_linux64.bin..."
mv "$SOURCE_FILE" "$RENAMED_FILE"

# Check if renaming was successful
if [ ! -f "$RENAMED_FILE" ]; then
    echo "[ ERROR ] Failed to rename main.bin to deoryz_wallet_searcher_latest_linux64.bin!"
    exit 1
fi



echo "Transfer successful!"
