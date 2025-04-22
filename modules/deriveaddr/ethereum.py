# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------
import sys
from bip_utils import Bip44Changes, Bip44Coins, Bip44

if __name__ == "__main__":
    from base import CryptoBase # base class for all wallets
else:
    from .base import CryptoBase # base class for all wallets

class EthereumWallet(CryptoBase):
    """Wallet class for Ethereum."""
    def get_private_key(self):
        # Derive the ETH address
        bip44_mst = Bip44.FromSeed(self.seed, Bip44Coins.ETHEREUM)
        bip44_acc = bip44_mst.Purpose().Coin().Account(self.account).Change(Bip44Changes.CHAIN_EXT)
        bip44_addr = bip44_acc.AddressIndex(self.index)  # First address index

        # Get private key in WIF format
        private_key_wif = bip44_addr.PrivateKey().ToWif()

        return private_key_wif

    def generate_address(self):
        """Generate a Bech32 Bitcoin address."""

        # Derive the ETH address
        bip44_mst = Bip44.FromSeed(self.seed, Bip44Coins.ETHEREUM)
        bip44_acc = bip44_mst.Purpose().Coin().Account(self.account).Change(Bip44Changes.CHAIN_EXT)  # External chain (receiving addresses)
        bip44_addr = bip44_acc.AddressIndex(self.index)  # First address index

        return bip44_addr.PublicKey().ToAddress()
    

if __name__ == "__main__":
    mnemonic = sys.argv[1]
    ethereum_wallet = EthereumWallet(mnemonic)
    ethereum_address = ethereum_wallet.generate_address()
    print(f"ETH Address: {ethereum_address}")