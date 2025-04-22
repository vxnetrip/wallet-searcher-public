# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------



from typing import List
from colorama import init as clinit, Fore as F

from bip_utils import Bip39MnemonicGenerator, Bip39WordsNum

from .deriveaddr import BitcoinWallet, EthereumWallet, TronWallet, \
                        LitecoinWallet, PolygonETH_Wallet, BNB_BSC_Wallet, \
                        XRP_Wallet, crypto_ids_map
from .balance import fetch_eth_balance, fetch_litecoin_balance, fetch_bitcoin_balance, \
                     fetch_tron_balance, fetch_polygon_balance, fetch_bnb_balance, \
                     fetch_xrp_balance, convert_crypto_to_usd

from . import loadConfig, TL

clinit(autoreset=True)

config = loadConfig()

# class to store the balance of found crypto
class CryptoWallet:
    def __init__(self) -> None:
        self.total_usd = 0
        self.btc = 0
        self.ltc = 0
        self.eth = 0
        self.trx = 0
        self.matic = 0
        self.bnb = 0
        self.xrp = 0

    def anyNonZero(self):
        return any(
            [
                bal != 0 for bal in [
                    self.btc, 
                    self.ltc, 
                    self.eth, 
                    self.trx, 
                    self.matic, 
                    self.bnb, 
                    self.xrp
                ]
            ]
        )

# Main program class
class Deoryz:
    def __init__(self) -> None:
        pass

    def _generateMnemonic(self):
        return Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_24 if config['mnemonicWords'] == 24 else Bip39WordsNum.WORDS_NUM_12)

    def _deriveAddress(self, mnemonic: str, network: str, account: int = 0, index: int = 0):
        """If mnemonic is None mnemonic will be generated automaticly"""
        match network:
            case "bitcoin":
                wallet = BitcoinWallet(mnemonic, account, index)
                return wallet.generate_address(), wallet.get_private_key()
            case "litecoin":
                wallet = LitecoinWallet(mnemonic, account, index)
                return wallet.generate_address(), wallet.get_private_key()
            case "ethereum":
                wallet = EthereumWallet(mnemonic, account, index)
                return wallet.generate_address(), wallet.get_private_key()
            case "tron":
                wallet = TronWallet(mnemonic, account, index)
                return wallet.generate_address(), wallet.get_private_key()
            case "polygon_eth":
                wallet = PolygonETH_Wallet(mnemonic, account, index)
                return wallet.generate_address(), wallet.get_private_key()
            case "bnb_bsc":
                wallet = BNB_BSC_Wallet(mnemonic, account, index)
                return wallet.generate_address(), wallet.get_private_key()
            case "xrp":
                wallet = XRP_Wallet(mnemonic, account, index)
                return wallet.generate_address(), wallet.get_private_key()
        return "Invalid Network"
    

    def _checkAddressBalance(self, network: str, address: str) -> float:
        match network:
            case "bitcoin":
                source, balance_btc = fetch_bitcoin_balance(address)
                if balance_btc is not None:
                    return balance_btc
                else:
                    print("All requests failed")
                    return -1
            case "litecoin":
                source, balance_ltc = fetch_litecoin_balance(address)
                if balance_ltc is not None:
                    return balance_ltc
                else:
                    print("All requests failed")
                    return -1
            case "ethereum":
                source, balance_eth = fetch_eth_balance(address)
                if balance_eth is not None:
                    return balance_eth
                else:
                    print("All requests failed")
                    return -1
            case "tron":
                source, balance_tron = fetch_tron_balance(address)
                if balance_tron is not None:
                    return balance_tron
                else:
                    print("All requests failed")
                    return -1
            case "polygon_eth":
                source, balance_matic = fetch_polygon_balance(address)
                if balance_matic is not None:
                    return balance_matic
                else:
                    print("All requests failed")
                    return -1
            case "bnb_bsc":
                source, balance_bnb = fetch_bnb_balance(address)
                if balance_bnb is not None:
                    return balance_bnb
                else:
                    print("All requests failed")
                    return -1
            case "xrp":
                source, balance_xrp = fetch_xrp_balance(address)
                if balance_xrp is not None:
                    return balance_xrp
                else:
                    print("All requests failed")
                    return -1
        return "Invalid Network"
    
                
    def start_searcher(self, amount: int = 20, account: int = 0, index: int = 0):
        counter = 0
        while True:
            mnemonic = self._generateMnemonic()
            output = f"{F.CYAN}[ {mnemonic} ]{F.WHITE} | "
            wallet = CryptoWallet()
            data_to_save = []
            for network in config['networks']:
                genetated_addr, addr_private_key = self._deriveAddress(mnemonic, network, account, index)
                match network:
                    case "bitcoin":
                        balance = self._checkAddressBalance(network, genetated_addr)
                        TL.pushLog(f"sessionID: {counter} | {mnemonic} | Derived {crypto_ids_map[network]} address: {genetated_addr} | Account: {account} | Index: {index} | ADDRESS BALANCE: {f'{balance}' if balance != -1 else 'FAILED TO FETCH ALL APIS RATE LIMITED'}")
                        if balance != -1:
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
                    case "litecoin":
                        balance = self._checkAddressBalance(network, genetated_addr)
                        TL.pushLog(f"sessionID: {counter} | {mnemonic} | Derived {crypto_ids_map[network]} address: {genetated_addr} | Account: {account} | Index: {index} | ADDRESS BALANCE: {f'{balance}' if balance != -1 else 'FAILED TO FETCH ALL APIS RATE LIMITED'}")
                        if balance != -1:
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

                    case "ethereum":
                        balance = self._checkAddressBalance(network, genetated_addr)
                        TL.pushLog(f"sessionID: {counter} | {mnemonic} | Derived {crypto_ids_map[network]} address: {genetated_addr} | Account: {account} | Index: {index} | ADDRESS BALANCE: {f'{balance}' if balance != -1 else 'FAILED TO FETCH ALL APIS RATE LIMITED'}")
                        if balance != -1:
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
                    case "tron":
                        balance = self._checkAddressBalance(network, genetated_addr)
                        TL.pushLog(f"sessionID: {counter} | {mnemonic} | Derived {crypto_ids_map[network]} address: {genetated_addr} | Account: {account} | Index: {index} | ADDRESS BALANCE: {f'{balance}' if balance != -1 else 'FAILED TO FETCH ALL APIS RATE LIMITED'}")
                        if balance != -1:
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

                    case "polygon_eth":
                        balance = self._checkAddressBalance(network, genetated_addr)
                        TL.pushLog(f"sessionID: {counter} | {mnemonic} | Derived {crypto_ids_map[network]} address: {genetated_addr} | Account: {account} | Index: {index} | ADDRESS BALANCE: {f'{balance}' if balance != -1 else 'FAILED TO FETCH ALL APIS RATE LIMITED'}")
                        if balance != -1:
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

                    case "bnb_bsc":
                        balance = self._checkAddressBalance(network, genetated_addr)
                        TL.pushLog(f"sessionID: {counter} | {mnemonic} | Derived {crypto_ids_map[network]} address: {genetated_addr} | Account: {account} | Index: {index} | ADDRESS BALANCE: {f'{balance}' if balance != -1 else 'FAILED TO FETCH ALL APIS RATE LIMITED'}")
                        if balance != -1:
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
                    
                    case "xrp":
                        balance = self._checkAddressBalance(network, genetated_addr)
                        TL.pushLog(f"sessionID: {counter} | {mnemonic} | Derived {crypto_ids_map[network]} address: {genetated_addr} | Account: {account} | Index: {index} | ADDRESS BALANCE: {f'{balance}' if balance != -1 else 'FAILED TO FETCH ALL APIS RATE LIMITED'}")
                        if balance != -1:
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
                            
                    case _:
                        print("Invalid network.")

            print(output) # prints formed output

            if wallet.anyNonZero():
                input(f"{F.LIGHTRED_EX}<!> [BALANCE FOUND] <!>{F.RESET}")
            
            counter += 1

            if counter == amount:
                break