# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------


import sys

if __name__ == "__main__":
    from apis import get_random_token, ETHERSCAN_TOKENS
    from proxyconnector import StealthConnection
else:
    from .apis import get_random_token, ETHERSCAN_TOKENS
    from .proxyconnector import StealthConnection

c = StealthConnection()

def convert_to_eth(wei_amount):
    return wei_amount / 1_000_000_000_000_000_000  # 1 ETH = 10^18 Wei

def fetch_from_etherscan(address):
    token = get_random_token(ETHERSCAN_TOKENS)
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={token}"
    response = c.session().get(url)
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get("status") == "1":
            balance_wei = int(response_json.get('result', 0))  # Etherscan returns balance in Wei
            return convert_to_eth(balance_wei)
        else:
            return None
    return None

def fetch_eth_balance(address):
    try:
        balance_eth = fetch_from_etherscan(address)
        if balance_eth is not None:
            return "etherscan", balance_eth
        else:
            # print(f"fetch_from_etherscan did not succeed")
            pass
    except Exception as e:
        # print(f"Request to fetch_from_etherscan failed: {e}")
        pass
    
    return None, None  # Return None if the request fails

if __name__ == "__main__":
    # Example usage
    address = sys.argv[1]  # Provide the ETH address as a command-line argument
    if address.startswith("0x"):  # Ethereum addresses typically start with '0x'
        source, balance_eth = fetch_eth_balance(address)

        if balance_eth is not None:
            print(f"Balance fetched from {source}: {balance_eth} ETH")
        else:
            print("Request failed or no balance found for ETH.")
    else:
        print("Invalid Ethereum address format.")