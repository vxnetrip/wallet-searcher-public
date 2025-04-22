# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------

import random

from .apis import get_random_token, \
                CRYPTOAPIS_TOKENS, \
                BLOCKCYPHER_TOKENS, \
                NOWNODES_TOKENS
from .proxyconnector import StealthConnection

c = StealthConnection()

def convert_to_ltc(satoshis_amount):
    return satoshis_amount / 100_000_000

def fetch_from_blockchair(address):
    session = c.session()
    url = f"https://api.blockchair.com/litecoin/dashboards/address/{address}"
    response = session.get(url)
    jsonresp = response.json()
    if jsonresp.get("data") is not None:
        balance_satoshis = jsonresp.get('data', {}).get(address, {}).get('address', {}).get('balance')
        return convert_to_ltc(balance_satoshis)
    return None


def fetch_from_cryptoid(address):
    session = c.session()
    url = f"http://chainz.cryptoid.info/ltc/api.dws?q=getbalance&a={address}"
    response = session.get(url)
    # print(response.text)
    try:
        balance_ltc = float(response.text)
        return balance_ltc
    except ValueError:
        return None

def fetch_from_blockcypher(address):
    session = c.session()
    token = get_random_token(BLOCKCYPHER_TOKENS)
    url = f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}/balance?token={token}"
    # url = f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}/balance"
    response = session.get(url)
    jsonresp = response.json()
    balance_satoshis = jsonresp.get('balance', None)
    if balance_satoshis is not None:
        return convert_to_ltc(balance_satoshis)
    return None

# This api requires api key
def fetch_from_nownodes(address):
    api_key = get_random_token(NOWNODES_TOKENS)
    headers = {
        'api-key': api_key
    }
    session = c.session(headers)
    api_key = get_random_token(NOWNODES_TOKENS)
    url = f'https://ltcbook.nownodes.io/api/v2/address/{address}'
    response = session.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            balance = float(data['balance'])
        except:
            return None
        return convert_to_ltc(balance)
    return None

def fetch_from_cryptoapis(address):
    """
    Fetches the balance of a given address from CryptoAPIs.
    """
    url = f"https://rest.cryptoapis.io/v2/blockchain-data/mainnet/litecoin/addresses/{address}/balance"

    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': get_random_token(CRYPTOAPIS_TOKENS)
    }
    session = c.session(headers)

    try:
        response = session.get(url)

        if response.status_code == 200:
            balance_data = response.json()
            try:
                balance = balance_data['data']['item']['balance']
            except:
                return None
            return balance
        else:
            return None
    
    except Exception as e:
        # return f"Exception occurred: {str(e)}"
        return None




# Function to sequentially try each service
def fetch_litecoin_balance(address):
    PAIDAPIS_fetch_functions = [
        fetch_from_blockcypher,
        fetch_from_cryptoapis,
        fetch_from_nownodes
    ]
    FREEAPIS_fetch_functions = [
        fetch_from_blockchair,
        fetch_from_cryptoid,
    ]

    fetch_functions = PAIDAPIS_fetch_functions + FREEAPIS_fetch_functions

    random.shuffle(fetch_functions)

    for fetch_function in fetch_functions:
        try:
            balance_ltc = fetch_function(address)
            if balance_ltc is not None:
                return fetch_function.__name__, balance_ltc
            else:
                pass
            
        except Exception as e:
            # print(f"Request to {fetch_function.__name__} failed: {e}")
            continue  # Try the next API if this one fails

    return None, None  # Return None if all requests fail