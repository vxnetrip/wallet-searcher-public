# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
__program__ = "wallet_searcher"
__version__ = "1.1.1"
__latest__ = "1.1.1" # FOR INTEGRITY
# ----------------------------------------------------------------------------

from colorama import Fore, init as colorama_init

colorama_init(autoreset=True)

import json, sys

from vendor.setup import Setup
# from vendor.protector import Protector

# Protector().run()
Setup().run()

def parseConfig(config_file = "./input/config.json"):
    data = None
    with open(config_file, "r+") as f:
        data = f.read()
    try:
        config = json.loads(data)
        return config
    except:
        print(f"{Fore.CYAN}[ {Fore.RED}JSON CONFIG INVALID {Fore.CYAN}] {Fore.LIGHTWHITE_EX}Configuration file have errors, please check config.json syntax and relaunch program")
        input(f"{Fore.LIGHTBLACK_EX}PRESS ANY KEY TO CONTINUE{Fore.RESET}")
        sys.exit(90284)

# from vendor.vxauth import VXNET_AUTHENTICATION_SYSTEM, getLatestProgramVersion

# auth_api = VXNET_AUTHENTICATION_SYSTEM()
config = parseConfig()

# Protector().run()

# json_auth_data = auth_api.authenticate(
#     __program__,
#     "./input/config.json",
#     "license"
# )

# Protector().run()

# __latest__ = getLatestProgramVersion(__program__)

# Protector().run()
json_auth_data = {
    "hwid": "",
    "expiration_date": "LIFETIME"
}
# Load everything
from modules import UI

if __name__ == "__main__":
    ui = UI(json_auth_data, __version__, __latest__)

    try:
        ui.main()
    except KeyboardInterrupt:
        sys.exit()