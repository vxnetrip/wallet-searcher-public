# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------


from .bitcoin import fetch_bitcoin_balance # BTC
from .ethereum import fetch_eth_balance # ETH
from .litecoin import fetch_litecoin_balance # LTC
from .tron import fetch_tron_balance # TRX
from .polygon_eth import fetch_polygon_balance # MATIC
from .bnb_bsc import fetch_bnb_balance # BNB
from .xrp import fetch_xrp_balance # XRP

from .currency_converter import convert_crypto_to_usd # Convert currencies

__all__ = [
    "fetch_bitcoin_balance",
    "fetch_eth_balance",
    "fetch_litecoin_balance",
    "fetch_tron_balance",
    "fetch_polygon_balance",
    "fetch_bnb_balance",
    "fetch_xrp_balance",

    "convert_crypto_to_usd"
]