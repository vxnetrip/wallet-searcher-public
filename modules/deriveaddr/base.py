# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------

from bip_utils import Bip39SeedGenerator, Bip39Languages

from .. import loadConfig

config = loadConfig()

class CryptoBase:
    """Base class for all cryptocurrency wallets."""
    def __init__(self, mnemonic: str, account: int = 0, index: int = 0) -> None:

        self.mnemonic = mnemonic
        self.seed = Bip39SeedGenerator(self.mnemonic, Bip39Languages.ENGLISH).Generate()

        self.account = account
        self.index = index