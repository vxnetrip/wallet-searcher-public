# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------

import sys
from bip_utils import Bip44, Bip44Coins, Bip44Changes


if __name__ == "__main__":
    from base import CryptoBase # base class for all wallets
else:
    from .base import CryptoBase # base class for all wallets

class LitecoinWallet(CryptoBase):
    """Wallet class for Litecoin using P2PKH addresses."""
    def get_private_key(self):
        """Get Litecoin address private key."""
        bip44_mst = Bip44.FromSeed(self.seed, Bip44Coins.LITECOIN)
        bip44_acc = bip44_mst.Purpose().Coin().Account(self.account).Change(Bip44Changes.CHAIN_EXT)
        bip44_addr = bip44_acc.AddressIndex(self.index)  # First address index

        # Get private key in WIF format
        private_key_wif = bip44_addr.PrivateKey().ToWif()

        return private_key_wif
    

    def generate_address(self):
        """Generate a Litecoin address."""

        # Derive the BIP44 account for Litecoin
        bip44_mst = Bip44.FromSeed(self.seed, Bip44Coins.LITECOIN)
        bip44_acc = bip44_mst.Purpose().Coin().Account(self.account).Change(Bip44Changes.CHAIN_EXT)  # External chain (receiving addresses)
        bip44_addr = bip44_acc.AddressIndex(self.index)  # First address index

        # Return the Bech32 (P2WPKH) address
        return bip44_addr.PublicKey().ToAddress()
    

if __name__ == "__main__":
    mnemonic = sys.argv[1]
    litecoin_wallet = LitecoinWallet(mnemonic)
    litecoin_address = litecoin_wallet.generate_address()
    print("Litecoin Address:", litecoin_address)