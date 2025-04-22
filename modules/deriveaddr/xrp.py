# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------

from xrpl.wallet import Wallet
from bip32 import BIP32
import sys

if __name__ == "__main__":
    from base import CryptoBase # base class for all wallets
else:
    from .base import CryptoBase # base class for all wallets

class XRP_Wallet(CryptoBase):
    """Wallet class for XRP."""
    def get_private_key(self):
        """Get XRP address private key."""
        bip32 = BIP32.from_seed(self.seed)

        # m/44'/144'/0'/0/0 (where 0 is the account index)
        private_key = bip32.get_privkey_from_path("m/44'/144'/0'/0/0")
        return private_key.hex()
    
    def generate_address(self):
        """Generate an XRP address."""
        bip32 = BIP32.from_seed(self.seed)

        # m/44'/144'/0'/0/0 (where 0 is the account index)
        private_key = bip32.get_privkey_from_path("m/44'/144'/0'/0/0")
        public_key = bip32.get_pubkey_from_path("m/44'/144'/0'/0/0")

        # Step 5: Generate XRP address from public key
        xrp_address = Wallet(public_key.hex(), private_key.hex()).classic_address
        return xrp_address

if __name__ == "__main__":
    mnemonic = sys.argv[1]
    xrp_wallet = XRP_Wallet(mnemonic)
    xrp_address = xrp_wallet.generate_address()
    print(f"XRP Address: {xrp_address}")