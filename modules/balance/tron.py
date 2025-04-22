# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------


import sys
import random
from .apis import get_random_token, TRONGRID_TOKENS, TRONSCAN_TOKENS
from .proxyconnector import StealthConnection
from .. import config

c = StealthConnection()

def convert_to_trx(sun_amount):
    return sun_amount / 1_000_000

def fetch_from_tronscan(address):
    token = get_random_token(TRONSCAN_TOKENS)
    url = f"https://apilist.tronscan.org/api/account?address={address}"
    headers = {"TRONSCAN-API-KEY": token}
    response = c.session(headers).get(url)
    if response.status_code == 200:
        response_json = response.json()
        balance_sun = response_json.get('balance', None)
        if balance_sun == None:
            return None
        return convert_to_trx(balance_sun)
    return None

def fetch_from_trongrid(address):
    token = get_random_token(TRONGRID_TOKENS)
    url = f"https://api.trongrid.io/v1/accounts/{address}"
    headers = {"TRON-PRO-API-KEY": token}
    response = c.session(headers).get(url)
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get("success") == True:
            data = response_json.get('data')
            if data and len(data) > 0:
                balance_sun = data[0].get('balance', 0)  # Default to 0 if balance is not found
                return convert_to_trx(balance_sun)
            else:
                return 0  # If there's no balance, return 0
        else:
            return None
    return None

# Function to sequentially try each service
def fetch_tron_balance(address):
    fetch_functions = [
        fetch_from_trongrid,
        fetch_from_tronscan
    ]

    random.shuffle(fetch_functions)

    for fetch_function in fetch_functions:
        try:
            balance_trx = fetch_function(address)
            if balance_trx is not None:
                return fetch_function.__name__, balance_trx
            else:
                # print(f"{fetch_function.__name__} did not succeed")
                pass
        except Exception as e:
            # print(f"Request to {fetch_function.__name__} failed: {e}")
            continue  # Try the next API if this one fails

    return None, None  # Return None if all requests fail