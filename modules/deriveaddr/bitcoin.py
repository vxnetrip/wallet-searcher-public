# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------

import sys
from bip_utils import Bip84, Bip84Coins, Bip44Changes

if __name__ == "__main__":
    from base import CryptoBase # base class for all wallets
else:
    from .base import CryptoBase # base class for all wallets
    
class BitcoinWallet(CryptoBase):
    """Wallet class for Bitcoin."""

    def get_private_key(self):
        # Derive the BIP84 account for Bitcoin (BIP84 is used for P2WPKH addresses)
        bip84_mst = Bip84.FromSeed(self.seed, Bip84Coins.BITCOIN)
        bip84_acc = bip84_mst.Purpose().Coin().Account(self.account).Change(Bip44Changes.CHAIN_EXT)
        bip84_addr = bip84_acc.AddressIndex(self.index)  # First address index

        # Get private key in WIF format
        private_key_wif = bip84_addr.PrivateKey().ToWif()

        return private_key_wif

    def generate_address(self):
        """Generate a Bech32 Bitcoin address."""

        # Derive the BIP84 account for Bitcoin (BIP84 is used for P2WPKH addresses)
        bip84_mst = Bip84.FromSeed(self.seed, Bip84Coins.BITCOIN)
        bip84_acc = bip84_mst.Purpose().Coin().Account(self.account).Change(Bip44Changes.CHAIN_EXT)  # External chain (receiving addresses)
        bip84_addr = bip84_acc.AddressIndex(self.index)  # First address index

        # Return the Bech32 (P2WPKH) address
        return bip84_addr.PublicKey().ToAddress()


# mnemonic = open("/home/vx/SALT.txt").readlines()[0].strip()

if __name__ == "__main__":
    mnemonic = sys.argv[1]
    bitcoin_wallet = BitcoinWallet(mnemonic)
    bitcoin_address = bitcoin_wallet.generate_address()
    print("Bitcoin Address:", bitcoin_address)
