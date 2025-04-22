# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------


import requests

# THIS NEEDS TO BE CHANGED DUE TO RATE LIMITS
# https://api.binance.com/api/v3/ticker/price?symbol=XRPUSDT NEW API WITHOUT RATE LIMITS
def get_crypto_prices(crypto_ids):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': ','.join(crypto_ids),
        'vs_currencies': 'usd'
    }
    response = requests.get(url, params=params)
    if response.status_code == 429:
        return 429
    return response.json()

def convert_crypto_to_usd(crypto_amount, crypto_id):
    prices = get_crypto_prices([crypto_id])
    if prices == 429:
        return 'FAILED'
    price_in_usd = prices[crypto_id]['usd']
    return round(crypto_amount * price_in_usd, 2)