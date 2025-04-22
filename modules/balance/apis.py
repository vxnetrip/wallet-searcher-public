# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------


import random
import sys
from colorama import Fore, init as colorama_init

from .. import config

colorama_init(autoreset=True)

BLOCKCYPHER_TOKENS = config['api_keys']['BLOCKCYPHER_TOKENS']
CRYPTOAPIS_TOKENS = config['api_keys']['CRYPTOAPIS_TOKENS']
TRONSCAN_TOKENS = config['api_keys']['TRONSCAN_TOKENS']
TRONGRID_TOKENS = config['api_keys']['TRONGRID_TOKENS']
ETHERSCAN_TOKENS = config['api_keys']['ETHERSCAN_TOKENS']
NOWNODES_TOKENS = config['api_keys']['NOWNODES_TOKENS']
BSCSCAN_TOKENS = config['api_keys']['BSCSCAN_TOKENS']

# Function to get random token
def get_random_token(tokenslist: list[str]) -> str:
    if len(tokenslist) > 0:
        realtokens = []
        for token in tokenslist:
            if token != "":
                realtokens.append(token)

        if len(realtokens) == 0:
            print(f"{Fore.YELLOW}[ {Fore.RED}CONFIG {Fore.YELLOW}] {Fore.LIGHTRED_EX}Please insert at least one key from each website for mnemonic checks")
            input("PRESS ENTER TO EXIT")
            sys.exit(4)

        return random.choice(realtokens)
    else:
        print(f"{Fore.YELLOW}[ {Fore.RED}CONFIG {Fore.YELLOW}] {Fore.LIGHTRED_EX}Please insert at least one key from each website for mnemonic checks")
        input("PRESS ENTER TO EXIT")
        sys.exit()