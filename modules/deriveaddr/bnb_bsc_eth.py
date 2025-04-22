# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------


# BNB Smart Chain (BNB) on Eth network
import sys

if __name__ == "__main__":
    from ethereum import EthereumWallet as BNB_BSC_Wallet # BECAUSE IT IS ON ETHEREUM NETOWORK
else:
    from .ethereum import EthereumWallet as BNB_BSC_Wallet # BECAUSE IT IS ON ETHEREUM NETOWORK

# ----------------------------------------------------
# NOTE: BNB Smart Chain is based on ETHEREUM network
# To avoid duplicating code we are importing it

if __name__ == "__main__":
    mnemonic = sys.argv[1]
    ethereum_wallet = BNB_BSC_Wallet(mnemonic)
    ethereum_address = ethereum_wallet.generate_address()
    print(f"BNB Smart Chain Address: {ethereum_address}")