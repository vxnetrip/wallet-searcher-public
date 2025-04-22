# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------


import random
import sys

from .apis import get_random_token, \
                CRYPTOAPIS_TOKENS, \
                BLOCKCYPHER_TOKENS, \
                NOWNODES_TOKENS
                
from .proxyconnector import StealthConnection
from .. import config
    

c = StealthConnection()

def convert_to_btc(satoshis_amount):
    return satoshis_amount / 100_000_000

def fetch_from_blockchain(address):
    url = f"https://blockchain.info/balance?active={address}"
    response = c.session().get(url)
    if response.status_code == 200:
        data = response.json()
        if address in data:
            balance_satoshi = data[address]["final_balance"]
            balance_btc = convert_to_btc(balance_satoshi)  # Convert satoshi to BTC
            return balance_btc
        else:
            return None
    else:
        # print(f"Request failed with status code of: {response.status_code}")
        pass
    return None

# This api has limits so you need to use proxies to avoid rate limits
def fetch_from_blockchair(address):
    url = f"https://api.blockchair.com/bitcoin/dashboards/address/{address}"
    response = c.session().get(url)
    if response.status_code == 200:
        data = response.json()
        if address in data:
            balance_satoshi = data[address]["final_balance"]
            balance_btc = convert_to_btc(balance_satoshi)  # Convert satoshi to BTC
            return balance_btc
        else:
            return None
    else:
        # print(f"Request failed with status code of: {response.status_code}")
        pass
    return None

def fetch_from_blockstream(address):
    url = f"https://blockstream.info/api/address/{address}"
    response = c.session().get(url)
    if response.status_code == 200:
        chain_stats = response.json().get('chain_stats')
        if chain_stats is not None:
            funded_txo_sum = chain_stats.get('funded_txo_sum', 0)
            spent_txo_sum = chain_stats.get('spent_txo_sum', 0)
            balance_satoshis = funded_txo_sum - spent_txo_sum
            return convert_to_btc(balance_satoshis)
    else:
        print(f"Request failed with status code: {response.status_code}")
    return None

def fetch_from_mempool(address):
    url = f"https://mempool.space/api/address/{address}"
    response = c.session().get(url)
    if response.status_code == 200:
        chain_stats = response.json().get('chain_stats')
        if chain_stats is not None:
            funded_txo_sum = chain_stats.get('funded_txo_sum', 0)
            spent_txo_sum = chain_stats.get('spent_txo_sum', 0)
            balance_satoshis = funded_txo_sum - spent_txo_sum
            return convert_to_btc(balance_satoshis)
    else:
        # print(f"Request failed with status code of: {response.status_code}")
        pass
    return None

def fetch_from_cryptoid(address):
    url = f"https://chainz.cryptoid.info/btc/api.dws?q=getbalance&a={address}"
    response = c.session().get(url)
    if response.status_code == 200:
        try:
            balance_btc = float(response.text)
            return balance_btc
        except ValueError:
            return None
    else:
        # print(f"Request failed with status code of: {response.status_code}")
        pass

def fetch_from_bitcore(address):
    url = f"https://api.bitcore.io/api/BTC/mainnet/address/{address}"
    response = c.session().get(url)
    if response.status_code == 200:
        balance_btc = response.json().get('balance')
        if balance_btc is not None:
            return balance_btc
    else:
        # print(f"Request failed with status code of: {response.status_code}")
        pass
    return None

# This api requires api key
def fetch_from_cryptoapis(address):
    url = f"https://api.cryptoapis.io/v1/bc/btc/mainnet/address/{address}/balance"
    headers = {"X-API-Key": get_random_token(CRYPTOAPIS_TOKENS)}  # Replace with your actual API key
    response = c.session(headers).get(url)
    if response.status_code == 200:
        balance_btc = response.json().get('payload', {}).get('balance')
        if balance_btc is not None:
            return balance_btc
    else:
        # print(f"Request failed with status code of: {response.status_code}")
        pass
    return None

# This api requires api key
def fetch_from_blockcypher(address):
    token = get_random_token(BLOCKCYPHER_TOKENS)
    url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance?token={token}"
    response = c.session().get(url)
    if response.status_code == 200:
        balance_satoshis = response.json().get('balance')
        if balance_satoshis is not None:
            return convert_to_btc(balance_satoshis)
    else:
        # print(f"Request failed with status code of: {response.status_code}")
        pass
    return None

# This api requires api key
def fetch_from_nownodes(address):
    api_key = get_random_token(NOWNODES_TOKENS)
    url = f'https://btcbook.nownodes.io/api/v2/address/{address}'
    headers = {
        'api-key': api_key
    }
    response = c.session(headers).get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            balance = float(data['balance'])
        except:
            return None
        return convert_to_btc(balance)
    return None




# Function to sequentially try each service
def fetch_bitcoin_balance(address):
    PAIDAPIS_fetch_functions = [
        fetch_from_blockcypher,
        fetch_from_cryptoapis,
        fetch_from_nownodes,
    ]
    FREEAPIS_fetch_functions = [
        fetch_from_blockchair,
        fetch_from_cryptoid,
        fetch_from_bitcore,
        fetch_from_blockstream,
        fetch_from_mempool,
    ]

    fetch_functions = PAIDAPIS_fetch_functions + FREEAPIS_fetch_functions

    random.shuffle(fetch_functions)

    for fetch_function in fetch_functions:
        try:
            balance_btc = fetch_function(address)
            if balance_btc is not None:
                return fetch_function.__name__, balance_btc
            else:
                # print(f"{fetch_function.__name__} returned no balance for this address.")
                pass

        except Exception as e:
            #print(f"Request to {fetch_function.__name__} failed: {e}")
            #raise e
            continue  # Try the next API if this one fails

    return None, None  # Return None if all requests fail

if __name__ == "__main__":
    # Example usage
    address = sys.argv[1] 
    source, balance_btc = fetch_bitcoin_balance(address)

    if balance_btc is not None:
        print(f"Balance fetched from {source}: {balance_btc} BTC")
    else:
        print("All requests failed or no balance found.")