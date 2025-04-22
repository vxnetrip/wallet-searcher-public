# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------


import json
import os
import ctypes

from colorama import Fore as F, Style, init as clinit
from threading import Lock
from datetime import datetime


clinit(autoreset=True)


CONFIG_PATH = os.path.join(os.getcwd(), "input", "config.json")

def loadConfig(config_path: str = CONFIG_PATH) -> dict:
    return json.load(open(config_path))

config = loadConfig()


lock = Lock()

class TL:
    def timestamp():
        return datetime.now().strftime("%H:%M:%S")
    

    def log(tag: str, content: any, color: str):
        ts = TL.timestamp()
        with lock:
            return print(
                f"{Style.BRIGHT}{F.WHITE}[{F.BLUE}{ts}{F.WHITE}][{color}{tag.upper()[:4]}{F.WHITE}] {F.GREEN}- {F.WHITE}{content}{Style.RESET_ALL}"
            )
        
    def pushLog(content: str, end: str='\n', filename: str = "./input/logs.log"):    
        '''Append the log line to file'''
        if config['saveLogs']:
            with lock:
                with open(filename, 'a+') as fl:
                    fl.write(f'{datetime.now().strftime(r"%d/%m/%Y - %H:%M:%S")} | {content}{end}')

    def saveWallet(mnemonic: str, seed: str, data: list[dict], filename: str = "./input/found_wallets.txt"):
        with lock:
            with open(filename, 'a+') as ww:
                ww.write(f'''
Found on {datetime.now().strftime(r"%d/%m/%Y - %H:%M:%S")}
Mnemonic {len(mnemonic.split())} words => {mnemonic}
Seed (hex) => {seed}
< Balance data >
''')

                for wallet in data:
                    ww.write(f"""
--------------------------------------------
Network => {wallet['network']}
Address => {wallet['address']}
Private Key => {wallet['private_key']}
Balance => {wallet['crypto_id']}: {wallet['balance_crypto']}
Balance USD => {wallet['balance_usd']}
--------------------------------------------
""")

                ww.write('''
-------------------------------------------------------------
''')

    def remove_content(filename: str, delete_line: str) -> None:
        '''Remove content from file'''
        with open(filename, "r+") as io:
            content = io.readlines()
            io.seek(0)
            for line in content:
                if not (delete_line in line):
                    io.write(line)
            io.truncate()

    def add_content(filename: str, content: str):
        '''Append to file'''
        with open(filename, "a+") as io:
            io.write(content + '\n')

    def update_console_title(new_title: str) -> None:
        '''Update console title Linux & Windows support'''
        if os.name == "nt":
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            ctypes.windll.kernel32.SetConsoleTitleW(new_title)
        else:
            print(f'\033]0;{new_title}\007')