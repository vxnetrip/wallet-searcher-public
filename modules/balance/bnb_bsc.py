# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------


# BNB - Binance Smart Chain (BSC)

from .apis import get_random_token, \
                BSCSCAN_TOKENS
                
from .proxyconnector import StealthConnection
from .. import config

c = StealthConnection()

# API_KEY = 'Q3EIPXQHU9C8GPN322XZ8X1RRR8YQCMF2W'
# example req: https://api.bscscan.com/api?module=account&action=balance&address=0x846E03A9954c377bfEbb160903277380b3c55EA8&tag=latest&apikey=Q3EIPXQHU9C8GPN322XZ8X1RRR8YQCMF2W

def fetch_from_bscscan(address):
    # 5 calls / second
    API_KEY = get_random_token(BSCSCAN_TOKENS)
    url = f"https://api.bscscan.com/api?module=account&action=balance&address={address}&tag=latest&apikey={API_KEY}"

    response = c.session().get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == '1':
            if 'result' in data:
                return int(data['result']) / 1e18  # Convert from wei to BNB
    else:
        # print(f"Request failed with status code of: {response.status_code}")
        pass
    return None


def fetch_bnb_balance(address):
    try:
        balance_bnb = fetch_from_bscscan(address)
        if balance_bnb is not None:
            return 'BSCScan', balance_bnb
        else:
            pass
    except Exception as e:
        pass
    
    return None, None  # Return None if the request fails
