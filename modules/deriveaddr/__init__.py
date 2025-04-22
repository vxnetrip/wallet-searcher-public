# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------

from .bitcoin import BitcoinWallet
from .litecoin import LitecoinWallet
from .ethereum import EthereumWallet
from .tron import TronWallet
from .polygon_eth import PolygonETH_Wallet
from .bnb_bsc_eth import BNB_BSC_Wallet
from .xrp import XRP_Wallet

crypto_ids_map = {
    'bitcoin': 'BTC',
    'litecoin': 'LTC',
    'ethereum': 'ETH',
    'tron': 'TRX',
    'polygon_eth': 'MATIC',
    'bnb_bsc': 'BNB',
    'xrp': 'XRP'
}

__all__ = [
    "BitcoinWallet", 
    "LitecoinWallet", 
    "EthereumWallet",
    "TronWallet",
    "PolygonETH_Wallet",
    "BNB_BSC_Wallet",
    "XRP_Wallet",

    "crypto_ids_map" # map network to cryptoID
]