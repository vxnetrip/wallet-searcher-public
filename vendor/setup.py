# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------


import os

class Setup:
    def __init__(self) -> None:
        self.inputdir = "./input"
        self.configpath = os.path.join("input", "config.json")
        self.files = [
            f"./{self.inputdir}/mnemonic_phrases.txt",
            f"./{self.inputdir}/logs.log",
            f"./{self.inputdir}/found_wallets.txt"
            # f"./{self.inputdir}/addresses.txt",
        ]
        self.default_config = """
{
    "license": "",
    "saveLogs": false,
    "mnemonicWords": 12,
    "networks": [
        "bitcoin",
        "litecoin",
        "tron",
        "ethereum",
        "polygon_eth",
        "bnb_bsc",
        "xrp"
    ],
    "#IMPORTANT": "Obtain api keys from this websites (Sign up and obtain token)",
    "#1": "https://blockcypher.com",
    "#2": "https://cryptoapis.io/",
    "#3": "https://tronscan.io/",
    "#4": "https://trongrid.io/",
    "#5": "https://etherscan.io/",
    "#6": "https://nownodes.io/",
    "#7": "https://bscscan.com/",

    "#BYPASS" : "If you dont want to use api just leave default, but it is HIGHLY RECOMMENDED to sign up to some apis (without this program will not work)",
    "api_keys": {
        "BLOCKCYPHER_TOKENS": [
            "API KEY HERE" 
        ],
        "CRYPTOAPIS_TOKENS": [
            "API KEY HERE" 
        ],
        "TRONSCAN_TOKENS": [
            "API KEY HERE" 
        ],
        "TRONGRID_TOKENS": [
            "API KEY HERE" 
        ],
        "ETHERSCAN_TOKENS": [
            "API KEY HERE" 
        ],
        "NOWNODES_TOKENS": [
            "API KEY HERE"
        ],
        "BSCSCAN_TOKENS": [
            "API KEY HERE"
        ]
    },
    "useProxy": false,
    "proxyfile": "input/proxies.txt"
}
"""

    def writeJSON(self):
        if not os.path.exists(self.configpath):
            with open(self.configpath, "w+") as f:
                f.write(self.default_config)

    def touchFiles(self):
        for filepath in self.files:
            if not os.path.exists(filepath):
                open(filepath, "w+").close()

    def run(self) -> None:
        if not os.path.exists(self.inputdir):
            os.mkdir(self.inputdir)
        self.touchFiles()
        self.writeJSON()