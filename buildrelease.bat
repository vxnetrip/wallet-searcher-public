@echo off
echo [ WORKER ] Building Release
set "USERNAME=%USERNAME%"
set "SOURCE_FILE=./main.exe"
set "RENAMED_FILE=./deoryz_wallet_searcher_latest_win64.exe"
set "PYTHON_SCRIPT=./main.py"

REM Check if main.exe exists, if not, build it using Nuitka
if not exist "%SOURCE_FILE%" (
    echo main.exe not found, building with Nuitka...
    nuitka --onefile --follow-imports --lto=yes --remove-output --include-package=xrpl --include-package=Crypto --include-package=coincurve --include-package=eth_hash --include-data-dir="C:/Users/%USERNAME%/AppData/Local/Programs/Python/Python312/Lib/site-packages/xrpl/core/binarycodec/definitions=xrpl/core/binarycodec/definitions/" --include-data-dir="C:/Users/%USERNAME%/AppData/Local/Programs/Python/Python312/Lib/site-packages/bip_utils/bip/bip39/wordlist=bip_utils/bip/bip39/wordlist" --jobs=8 ./main.py
    pause
    REM Check if build was successful
    if not exist "%SOURCE_FILE%" (
        echo Error: Failed to build main.exe!
        exit /b 1
    )
)

REM Rename main.exe to deoryz_wallet_searcher_latest_win64.exe
echo [ WORKER ] Renaming main.exe to deoryz_wallet_searcher_latest_win64.exe...
ren "%SOURCE_FILE%" "deoryz_wallet_searcher_latest_win64.exe"

REM Check if renaming was successful
if not exist "%RENAMED_FILE%" (
    echo [ ERROR ] Failed to rename main.exe to deoryz_wallet_searcher_latest_win64.exe!
    exit /b 1
)

echo [ + ] Build finished
