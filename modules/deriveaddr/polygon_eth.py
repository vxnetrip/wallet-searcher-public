# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------

# Polygon (MATIC) is based on ETHEREUM netowork
# To avoid duplicating code we are importing ETH Wallet as PolygonETH_Wallet

import sys

if __name__ == "__main__":
    from ethereum import EthereumWallet as PolygonETH_Wallet # BECAUSE IT IS ON ETHEREUM NETOWORK
else:
    from .ethereum import EthereumWallet as PolygonETH_Wallet # BECAUSE IT IS ON ETHEREUM NETOWORK



if __name__ == "__main__":
    mnemonic = sys.argv[1]
    ethereum_wallet = PolygonETH_Wallet(mnemonic)
    ethereum_address = ethereum_wallet.generate_address()
    print(f"Polygon address on eth network (MATIC): {ethereum_address}")