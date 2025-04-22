# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------


import os
import sys
import json
import asyncio
import time


from mnemonic import Mnemonic
from colorama import init as clinit, Fore as F
from rich.console import Console
from rich.table import Table
from concurrent.futures import ThreadPoolExecutor

from . import TL
from . import Deoryz, CryptoWallet
from .balance import convert_crypto_to_usd
from .deriveaddr import crypto_ids_map

from .proxy import run_checker, run_scraper

from . import loadConfig, CONFIG_PATH


clinit(autoreset=True)

config = loadConfig()

# -------------------------------
TOTAL_BTC_FOUND = 0
TOTAL_LTC_FOUND = 0
TOTAL_ETH_FOUND = 0
TOTAL_TRX_FOUND = 0
TOTAL_MATIC_FOUND = 0
TOTAL_BNB_FOUND = 0
TOTAL_XRP_FOUND = 0
# -------------------------------

# -------------------------------
TOTAL_BALANCE_USD = 0
WALLETS_CHECKED = 0
SUCCESS_REQUESTS = 0
FAIL_REQUESTS = 0
FOUND_NON_EMPTY_WALLETS = 0
# -------------------------------

def get_new_title():
    return F"WALLETS CHECKED: {WALLETS_CHECKED} | TOTAL: {TOTAL_BALANCE_USD}$ | ( BTC: {TOTAL_BTC_FOUND} | LTC: {TOTAL_LTC_FOUND} | ETH: {TOTAL_ETH_FOUND} | TRX: {TOTAL_TRX_FOUND} | MATIC: {TOTAL_MATIC_FOUND} | BNB: {TOTAL_BNB_FOUND} | XRP: {TOTAL_XRP_FOUND} )"


def checkMnemonicFromFile(filepath: str, account: int, index: int = 0) -> None:
    global TOTAL_BTC_FOUND, TOTAL_ETH_FOUND, TOTAL_LTC_FOUND, TOTAL_TRX_FOUND, \
           TOTAL_MATIC_FOUND, TOTAL_BNB_FOUND, TOTAL_XRP_FOUND
    global TOTAL_BALANCE_USD
    global SUCCESS_REQUESTS, FAIL_REQUESTS
    global WALLETS_CHECKED, FOUND_NON_EMPTY_WALLETS

    deoryz_instance = Deoryz()
    phrases = []
    with open(filepath, "r+") as f:
        for line in f.readlines():
            mnemonic = line.strip()
            phrases.append(mnemonic)
        f.close()

    if len(phrases) == 0:
        print(f"{F.LIGHTRED_EX}[ {F.LIGHTWHITE_EX}READ {F.LIGHTRED_EX}] {F.LIGHTRED_EX}No mnemonic phrases found! | Please input mnemonic phrases in {F.MAGENTA}{filepath}")
        return
 
    for mnemonic in phrases:
        output = f"{F.LIGHTBLUE_EX}<{WALLETS_CHECKED}> {F.CYAN}[ {mnemonic} ]{F.WHITE} | "
        wallet = CryptoWallet()
        
        data_to_save = []
        
        for network in config['networks']:
            genetated_addr, addr_private_key = deoryz_instance._deriveAddress(mnemonic, network, account, index)
            balance = deoryz_instance._checkAddressBalance(network, genetated_addr)

            match network:
                case "bitcoin":
                    if balance != -1:
                        SUCCESS_REQUESTS += 1
                        wallet.btc += balance
                        if balance > 0:
                            output += f"{F.LIGHTYELLOW_EX}{wallet.btc} {crypto_ids_map[network]} {F.WHITE}| "
                            balance_usd = convert_crypto_to_usd(balance, network)
                            wallet.total_usd += balance_usd
                            data_to_save.append(
                                {
                                    'network': network,
                                    'address': genetated_addr,
                                    'crypto_id': crypto_ids_map[network],
                                    'balance_usd': balance_usd,
                                    'balance_crypto': balance,
                                    'private_key': addr_private_key,
                                }
                            )
                            
                        else:
                            output += f"{F.LIGHTBLACK_EX}{wallet.btc} {crypto_ids_map[network]} {F.WHITE}| "
                    else:
                        FAIL_REQUESTS += 1
                case "litecoin":
                    if balance != -1:
                        SUCCESS_REQUESTS += 1
                        wallet.ltc += balance
                        if balance > 0:
                            output += f"{F.LIGHTMAGENTA_EX}{wallet.ltc} {crypto_ids_map[network]} {F.WHITE}| "
                            balance_usd = convert_crypto_to_usd(balance, network)
                            wallet.total_usd += balance_usd
                            data_to_save.append(
                                {
                                    'network': network,
                                    'address': genetated_addr,
                                    'crypto_id': crypto_ids_map[network],
                                    'balance_usd': balance_usd,
                                    'balance_crypto': balance,
                                    'private_key': addr_private_key,
                                }
                            )
                            
                        else:
                            output += f"{F.LIGHTBLACK_EX}{wallet.ltc} {crypto_ids_map[network]} {F.WHITE}| "
                    else:
                        FAIL_REQUESTS += 1
                case "ethereum":
                    if balance != -1:
                        SUCCESS_REQUESTS += 1
                        wallet.eth += balance
                        if balance > 0:
                            output += f"{F.LIGHTCYAN_EX}{wallet.eth} {crypto_ids_map[network]} {F.WHITE}| "
                            balance_usd = convert_crypto_to_usd(balance, network)
                            wallet.total_usd += balance_usd
                            data_to_save.append(
                                {
                                    'network': network,
                                    'address': genetated_addr,
                                    'crypto_id': crypto_ids_map[network],
                                    'balance_usd': balance_usd,
                                    'balance_crypto': balance,
                                    'private_key': addr_private_key,
                                }
                            )
                            
                        else:
                            output += f"{F.LIGHTBLACK_EX}{wallet.eth} {crypto_ids_map[network]} {F.WHITE}| "
                    else:
                        FAIL_REQUESTS += 1
                case "tron":
                    if balance != -1:
                        SUCCESS_REQUESTS += 1
                        wallet.trx += balance
                        if balance > 0:
                            output += f"{F.LIGHTRED_EX}{wallet.trx} {crypto_ids_map[network]} {F.WHITE}| "
                            balance_usd = convert_crypto_to_usd(balance, network)
                            wallet.total_usd += balance_usd
                            data_to_save.append(
                                {
                                    'network': network,
                                    'address': genetated_addr,
                                    'crypto_id': crypto_ids_map[network],
                                    'balance_usd': balance_usd,
                                    'balance_crypto': balance,
                                    'private_key': addr_private_key,
                                }
                            )
                            
                        else:
                            output += f"{F.LIGHTBLACK_EX}{wallet.trx} {crypto_ids_map[network]} {F.WHITE}| "
                    else:
                        FAIL_REQUESTS += 1
                case "polygon_eth":
                    if balance != -1:
                        SUCCESS_REQUESTS += 1
                        wallet.trx += balance
                        if balance > 0:
                            output += f"{F.LIGHTRED_EX}{wallet.trx} {crypto_ids_map[network]} {F.WHITE}| "
                            balance_usd = convert_crypto_to_usd(balance, 'polygon')
                            wallet.total_usd += balance_usd
                            data_to_save.append(
                                {
                                    'network': network,
                                    'address': genetated_addr,
                                    'crypto_id': crypto_ids_map[network],
                                    'balance_usd': balance_usd,
                                    'balance_crypto': balance,
                                    'private_key': addr_private_key,
                                }
                            )
                            
                        else:
                            output += f"{F.LIGHTBLACK_EX}{wallet.trx} {crypto_ids_map[network]} {F.WHITE}| "
                    else:
                        FAIL_REQUESTS += 1
                case "bnb_bsc":
                    if balance != -1:
                        SUCCESS_REQUESTS += 1
                        wallet.trx += balance
                        if balance > 0:
                            output += f"{F.LIGHTRED_EX}{wallet.trx} {crypto_ids_map[network]} {F.WHITE}| "
                            balance_usd = convert_crypto_to_usd(balance, 'binancecoin')
                            wallet.total_usd += balance_usd
                            data_to_save.append(
                                {
                                    'network': network,
                                    'address': genetated_addr,
                                    'crypto_id': crypto_ids_map[network],
                                    'balance_usd': balance_usd,
                                    'balance_crypto': balance,
                                    'private_key': addr_private_key,
                                }
                            )
                            
                        else:
                            output += f"{F.LIGHTBLACK_EX}{wallet.trx} {crypto_ids_map[network]} {F.WHITE}| "
                    else:
                        FAIL_REQUESTS += 1
                case "xrp":
                    if balance != -1:
                        SUCCESS_REQUESTS += 1
                        wallet.trx += balance
                        if balance > 0:
                            output += f"{F.LIGHTRED_EX}{wallet.trx} {crypto_ids_map[network]} {F.WHITE}| "
                            balance_usd = convert_crypto_to_usd(balance, network)
                            wallet.total_usd += balance_usd
                            data_to_save.append(
                                {
                                    'network': network,
                                    'address': genetated_addr,
                                    'crypto_id': crypto_ids_map[network],
                                    'balance_usd': balance_usd,
                                    'balance_crypto': balance,
                                    'private_key': addr_private_key,
                                }
                            )
                            
                        else:
                            output += f"{F.LIGHTBLACK_EX}{wallet.trx} {crypto_ids_map[network]} {F.WHITE}| "
                    else:
                        FAIL_REQUESTS += 1
                case _:
                    print("Invalid network.")

        balance_found_boolean = wallet.anyNonZero()

        if balance_found_boolean:
            TL.saveWallet(mnemonic, Mnemonic('english').to_seed(mnemonic), data_to_save)
            FOUND_NON_EMPTY_WALLETS += 1
            output += F"{F.LIGHTGREEN_EX}TOTAL: {wallet.total_usd}$"

            TOTAL_BTC_FOUND += wallet.btc
            TOTAL_ETH_FOUND += wallet.eth
            TOTAL_LTC_FOUND += wallet.ltc
            TOTAL_TRX_FOUND += wallet.trx
            TOTAL_MATIC_FOUND += wallet.matic
            TOTAL_BNB_FOUND += wallet.bnb
            TOTAL_XRP_FOUND += wallet.xrp

            TOTAL_BALANCE_USD += wallet.total_usd
            print(output)
            input(f"{F.LIGHTRED_EX}<!> [BALANCE FOUND] <!>{F.RESET}") # FREEZE ALL TASKS FOR A SECOND
        else:
            print(output)

        WALLETS_CHECKED += 1

        TL.update_console_title(get_new_title())


def GenerateAndCheckMnemonic():
    global TOTAL_BTC_FOUND, TOTAL_ETH_FOUND, TOTAL_LTC_FOUND, TOTAL_TRX_FOUND, \
           TOTAL_MATIC_FOUND, TOTAL_BNB_FOUND, TOTAL_XRP_FOUND
    global TOTAL_BALANCE_USD
    global SUCCESS_REQUESTS, FAIL_REQUESTS
    global WALLETS_CHECKED, FOUND_NON_EMPTY_WALLETS

    deoryz_instance = Deoryz()
    mnemonic = deoryz_instance._generateMnemonic()
    output = f"{F.LIGHTBLUE_EX}<{WALLETS_CHECKED}> {F.CYAN}[ {mnemonic} ]{F.WHITE} | "
    wallet = CryptoWallet()
    
    for network in config['networks']:
        genetated_addr, addr_private_key = deoryz_instance._deriveAddress(mnemonic, network, 0, 0, 0)
        balance = deoryz_instance._checkAddressBalance(network, genetated_addr)

        TL.pushLog(f"sessionID: {WALLETS_CHECKED} | {mnemonic} | Derived {network} address: {genetated_addr} | Account: 0 | Index: 0 | ADDRESS BALANCE: {f'{balance}' if balance != -1 else 'FAILED TO FETCH ALL APIS RATE LIMITED'}")
        
        data_to_save = []

        match network:
            case "bitcoin":
                if balance != -1:
                    SUCCESS_REQUESTS += 1
                    wallet.btc += balance
                    if balance > 0:
                        output += f"{F.LIGHTYELLOW_EX}{wallet.btc} {crypto_ids_map[network]} {F.WHITE}| "
                        balance_usd = convert_crypto_to_usd(balance, network)
                        wallet.total_usd += balance_usd
                        data_to_save.append(
                            {
                                'network': network,
                                'address': genetated_addr,
                                'crypto_id': crypto_ids_map[network],
                                'balance_usd': balance_usd,
                                'balance_crypto': balance,
                                'private_key': addr_private_key,
                            }
                        )
                    else:
                        output += f"{F.LIGHTBLACK_EX}{wallet.btc} {crypto_ids_map[network]} {F.WHITE}| "
                else:
                    FAIL_REQUESTS += 1
            case "litecoin":
                if balance != -1:
                    SUCCESS_REQUESTS += 1
                    wallet.ltc += balance
                    if balance > 0:
                        output += f"{F.LIGHTMAGENTA_EX}{wallet.ltc} {crypto_ids_map[network]} {F.WHITE}| "
                        balance_usd = convert_crypto_to_usd(balance, network)
                        wallet.total_usd += balance_usd
                        data_to_save.append(
                            {
                                'network': network,
                                'address': genetated_addr,
                                'crypto_id': crypto_ids_map[network],
                                'balance_usd': balance_usd,
                                'balance_crypto': balance,
                                'private_key': addr_private_key,
                            }
                        )
                    else:
                        output += f"{F.LIGHTBLACK_EX}{wallet.ltc} {crypto_ids_map[network]} {F.WHITE}| "
                else:
                    FAIL_REQUESTS += 1
            case "ethereum":
                if balance != -1:
                    SUCCESS_REQUESTS += 1
                    wallet.eth += balance
                    if balance > 0:
                        output += f"{F.LIGHTCYAN_EX}{wallet.eth} {crypto_ids_map[network]} {F.WHITE}| "
                        balance_usd = convert_crypto_to_usd(balance, network)
                        wallet.total_usd += balance_usd
                        data_to_save.append(
                            {
                                'network': network,
                                'address': genetated_addr,
                                'crypto_id': crypto_ids_map[network],
                                'balance_usd': balance_usd,
                                'balance_crypto': balance,
                                'private_key': addr_private_key,
                            }
                        )
                    else:
                        output += f"{F.LIGHTBLACK_EX}{wallet.eth} {crypto_ids_map[network]} {F.WHITE}| "
                else:
                    FAIL_REQUESTS += 1
            case "tron":
                if balance != -1:
                    SUCCESS_REQUESTS += 1
                    wallet.trx += balance
                    if balance > 0:
                        output += f"{F.LIGHTRED_EX}{wallet.trx} {crypto_ids_map[network]} {F.WHITE}| "
                        balance_usd = convert_crypto_to_usd(balance, network)
                        wallet.total_usd += balance_usd
                        data_to_save.append(
                            {
                                'network': network,
                                'address': genetated_addr,
                                'crypto_id': crypto_ids_map[network],
                                'balance_usd': balance_usd,
                                'balance_crypto': balance,
                                'private_key': addr_private_key,
                            }
                        )
                    else:
                        output += f"{F.LIGHTBLACK_EX}{wallet.trx} {crypto_ids_map[network]} {F.WHITE}| "
                else:
                    FAIL_REQUESTS += 1
            case "polygon_eth":
                if balance != -1:
                    SUCCESS_REQUESTS += 1
                    wallet.matic += balance
                    if balance > 0:
                        output += f"{F.LIGHTBLUE_EX}{wallet.matic} {crypto_ids_map[network]} {F.WHITE}| "
                        balance_usd = convert_crypto_to_usd(balance, 'polygon')
                        wallet.total_usd += balance_usd
                        data_to_save.append(
                            {
                                'network': network,
                                'address': genetated_addr,
                                'crypto_id': crypto_ids_map[network],
                                'balance_usd': balance_usd,
                                'balance_crypto': balance,
                                'private_key': addr_private_key,
                            }
                        )
                    else:
                        output += f"{F.LIGHTBLACK_EX}{wallet.matic} {crypto_ids_map[network]} {F.WHITE}| "
                else:
                    FAIL_REQUESTS += 1

            case "bnb_bsc":
                if balance != -1:
                    SUCCESS_REQUESTS += 1
                    wallet.bnb += balance
                    if balance > 0:
                        output += f"{F.YELLOW}{wallet.bnb} {crypto_ids_map[network]} {F.WHITE}| "
                        balance_usd = convert_crypto_to_usd(balance, 'binancecoin')
                        wallet.total_usd += balance_usd
                        data_to_save.append(
                            {
                                'network': network,
                                'address': genetated_addr,
                                'crypto_id': crypto_ids_map[network],
                                'balance_usd': balance_usd,
                                'balance_crypto': balance,
                                'private_key': addr_private_key,
                            }
                        )
                    else:
                        output += f"{F.LIGHTBLACK_EX}{wallet.bnb} {crypto_ids_map[network]} {F.WHITE}| "
                else:
                    FAIL_REQUESTS += 1
            
            case "xrp":
                if balance != -1:
                    SUCCESS_REQUESTS += 1
                    wallet.xrp += balance
                    if balance > 0:
                        output += f"{F.LIGHTMAGENTA_EX}{wallet.xrp} {crypto_ids_map[network]} {F.WHITE}| "
                        balance_usd = convert_crypto_to_usd(balance, network)
                        wallet.total_usd += balance_usd
                        data_to_save.append(
                            {
                                'network': network,
                                'address': genetated_addr,
                                'crypto_id': crypto_ids_map[network],
                                'balance_usd': balance_usd,
                                'balance_crypto': balance,
                                'private_key': addr_private_key,
                            }
                        )
                    else:
                        output += f"{F.LIGHTBLACK_EX}{wallet.xrp} {crypto_ids_map[network]} {F.WHITE}| "
                else:
                    FAIL_REQUESTS += 1

            case _:
                print("Invalid network.")
            

    balance_found_boolean = wallet.anyNonZero()

    if balance_found_boolean:
        TL.saveWallet(mnemonic, Mnemonic('english').to_seed(mnemonic), data_to_save)
        FOUND_NON_EMPTY_WALLETS += 1
        output += F"{F.LIGHTGREEN_EX}TOTAL USD: {wallet.total_usd}$"
        TOTAL_BTC_FOUND += wallet.btc
        TOTAL_ETH_FOUND += wallet.eth
        TOTAL_LTC_FOUND += wallet.ltc
        TOTAL_TRX_FOUND += wallet.trx
        TOTAL_BALANCE_USD += wallet.total_usd
        print(output)
        input(f"{F.LIGHTRED_EX}<!> [BALANCE FOUND] <!>{F.RESET}") # FREEZE ALL TASKS FOR A SECOND
    else:
        print(output)

    WALLETS_CHECKED += 1

    TL.update_console_title(get_new_title())

async def manage_tasks(executor, max_concurrent_tasks, total_tasks):
    loop = asyncio.get_event_loop()
    tasks_to_run = list(range(total_tasks))  # Generate a list of tasks
    futures = []
    
    # Start initial set of tasks
    for _ in range(min(max_concurrent_tasks, len(tasks_to_run))):
        task_id = tasks_to_run.pop(0)
        futures.append(loop.run_in_executor(executor, GenerateAndCheckMnemonic))
    
    while futures:
        # Wait for any task to complete
        done, pending = await asyncio.wait(futures, return_when=asyncio.FIRST_COMPLETED)
        
        # Process completed tasks
        for future in done:
            futures.remove(future)
        
        # As tasks finish, start new ones to maintain the limit
        while tasks_to_run and len(futures) < max_concurrent_tasks:
            task_id = tasks_to_run.pop(0)
            futures.append(loop.run_in_executor(executor, GenerateAndCheckMnemonic))

    # Await any remaining tasks to complete
    await asyncio.gather(*futures)


async def start_threaded_searcher(total_tasks: int = 20, max_concurrent_tasks: int = 3):
    with ThreadPoolExecutor(max_workers=max_concurrent_tasks) as executor:
        await manage_tasks(executor, max_concurrent_tasks, total_tasks)

class UI:
    def __init__(self, json_auth_data: dict, current_version: str, latest_version: str) -> None:
        self.expiration_date = json_auth_data.get('expiration_date')
        self.hwid = json_auth_data.get('hwid')
        self.current_version = current_version
        self.latest_version = latest_version

    def clearConsole(self):
        os.system("cls" if os.name == "nt" else "clear")

    def printlogo(self): 
        print(F.LIGHTRED_EX + """
                            ╦  ╔═╗╔═╗╔╦╗  """ + F.LIGHTYELLOW_EX + """╔╦╗╔═╗╔═╗╦═╗╦ ╦╔═╗
                            ║  ║ ║╚═╗ ║    """ + F.LIGHTRED_EX + """║║║╣ ║ ║╠╦╝╚╦╝╔═╝
                            ╩═╝╚═╝╚═╝ ╩   """ + F.LIGHTYELLOW_EX + """═╩╝╚═╝╚═╝╩╚═ ╩ ╚═╝
                                    """ + F.LIGHTBLUE_EX + """ Version """ + F.LIGHTCYAN_EX + self.current_version + """
                           """ + F.LIGHTBLUE_EX + """ License valid until """ + F.LIGHTMAGENTA_EX + self.expiration_date + """
                            """ + F.RED + """ <LOST CRYPTO WALLETS SEARCHER>
                            """ + F.RED + """       <DISCORD.GG/VXNET>
        """ + F.RESET)
        if self.current_version != self.latest_version:
            print(f"                          {F.LIGHTRED_EX}New update available! {F.LIGHTWHITE_EX}| {F.LIGHTMAGENTA_EX}{self.current_version} -> {self.latest_version}")
            print(f"                           {F.LIGHTYELLOW_EX}Download it from http://lefeu.nvnet.pl")

    def displayMenu(self):

        # Initialize the console
        console = Console()

        # Create the table
        table = Table(title=f"")

        # Define the columns
        table.add_column("Command", justify="left", style="cyan", no_wrap=True)
        table.add_column("Description", justify="left", style="magenta")

        # Add rows with command descriptions
        table.add_row("run-searcher", "Generate mnemonic phrases and check balance.")
        table.add_row("run-searcher-threaded", "Same as run-searcher but threaded.")
        table.add_row("check-mnemonic", "Check mnemonic from input/mnemonic_phrases.txt.")
        table.add_row("check-addresses_from_file (SOON!)", "COOMING SOON!!!!")

        table.add_row("proxy-scraper", "Run proxy scraper to scrape proxies from web.")
        table.add_row("proxy-checker", "Run proxy checker to find alive proxies.")

        table.add_row("clear", "Clear screen.")
        table.add_row("dconfig", "Display configuration settings.")
        table.add_row("exit", "Exit program")

        # Print the table to the console
        console.print(table)

    def shellCapture(self):
        try:
            login = os.getlogin()
        except:
            login = "ANY_USER"
        command = input(F.LIGHTMAGENTA_EX+ "deoryz" + F.LIGHTBLUE_EX + "@" + F.LIGHTRED_EX + login + ": " + F.LIGHTWHITE_EX)
        print(F.RESET, end='\r')
        return command

    def main(self):
        self.clearConsole()
        self.printlogo()
        self.displayMenu()
        while True:
            command = self.shellCapture()

            if command == "run-searcher":
                deoryz_instance = Deoryz()
                amount = input(f"{F.LIGHTGREEN_EX}<$> {F.YELLOW}Enter amount of mnemonic to scan (default = 20): ")
                if amount == "":
                    amount = 20
                TL.pushLog(f"Running {command} | Options: < amount: {amount} >")
                start_time = time.time()
                deoryz_instance.start_searcher(int(amount))
                # Calculate the total time taken
                total_time = time.time() - start_time

                # Convert the total time to H:M:S
                hours, remainder = divmod(total_time, 3600)  # 1 hour = 3600 seconds
                minutes, seconds = divmod(remainder, 60)     # 1 minute = 60 seconds
                TL.pushLog(f"Finished {command} | Total work time: {int(hours)}h {int(minutes)}m {int(seconds)}s")
                input(f"{F.LIGHTBLACK_EX}>>> PRESS ANY KEY TO CONTINUE <<<{F.RESET}")
                self.main()
                break
            elif command == "run-searcher-threaded":
                total_tasks = input(F"{F.LIGHTWHITE_EX}[ {F.LIGHTGREEN_EX}TASKS {F.LIGHTWHITE_EX}] {F.LIGHTYELLOW_EX}Enter amount of mnemonic to scan (default = 20):{F.LIGHTWHITE_EX} ")
                if total_tasks == "":
                    total_tasks = 20
                else:
                    total_tasks = int(total_tasks)

                max_concurrent_tasks = input(F"{F.LIGHTWHITE_EX}[ {F.LIGHTGREEN_EX}MAX THREADS {F.LIGHTWHITE_EX}] {F.LIGHTYELLOW_EX}Max threads (default = 3):{F.LIGHTWHITE_EX} ")

                if max_concurrent_tasks == "":
                    total_tasks = 3
                elif int(max_concurrent_tasks) > 3:
                    max_concurrent_tasks = int(max_concurrent_tasks)
                    print(f"{F.CYAN}[ {F.LIGHTYELLOW_EX}IMPORTANT | WARNING {F.CYAN}] {F.LIGHTYELLOW_EX}Too much threads will overload checking apis")
                else:
                    max_concurrent_tasks = int(max_concurrent_tasks)
                
                # print(f"{F.CYAN}[ {F.RED}TASKS {F.CYAN}] {F.LIGHTWHITE_EX}Virtual Machine Detected")
                print(f"{F.CYAN}[ {F.LIGHTMAGENTA_EX}HINT {F.CYAN}] {F.LIGHTWHITE_EX}To avoid rate limits it is recommended to put more api keys")
                input(f"{F.LIGHTBLACK_EX}>>> PRESS ANY KEY TO START <<<{F.RESET}")
                TL.pushLog(f"Running {command} | Options: < amount: {total_tasks} | max concurrent tasks: {max_concurrent_tasks} >")
                start_time = time.time()
                asyncio.run(start_threaded_searcher(int(total_tasks), int(max_concurrent_tasks)))
                # Calculate the total time taken
                total_time = time.time() - start_time
                # Convert the total time to H:M:S
                hours, remainder = divmod(total_time, 3600)  # 1 hour = 3600 seconds
                minutes, seconds = divmod(remainder, 60)     # 1 minute = 60 seconds
                TL.pushLog(f"Finished {command} | Total work time: {int(hours)}h {int(minutes)}m {int(seconds)}s")
                input(f"{F.LIGHTBLACK_EX}>>> PRESS ANY KEY TO CONTINUE <<<{F.RESET}")
                self.main()

            elif command == "check-mnemonic":
                account = input(f"{F.LIGHTGREEN_EX}<$> {F.YELLOW}Enter account to scan (default = 0): ")
                if account == "":
                    account = "0"
                index = input(f"{F.LIGHTGREEN_EX}<$> {F.YELLOW}Enter index to scan (default = 0): ")
                if index == "":
                    index = "0"
                checkMnemonicFromFile(os.path.join(os.getcwd(), "input", "mnemonic_phrases.txt"), int(account), int(index))
                input(f"{F.LIGHTBLACK_EX}>>> PRESS ANY KEY TO CONTINUE <<<{F.RESET}")
                self.main()
                break

            elif command == "proxy-scraper":
                run_scraper()

            elif command == "proxy-checker":
                run_checker()

            elif command == "dconfig":
                print(f"{F.GREEN}[ + ]{F.WHITE} Displaying config file {F.BLUE}({CONFIG_PATH})")
                print(F"{F.LIGHTBLACK_EX}{json.dumps(config, indent=4)}")

            elif command == "clear":
                self.main()
                break
            elif command == "exit":
                sys.exit()
            elif command == "":
                pass
            else:
                print(f"bash: {command}: command not found")
