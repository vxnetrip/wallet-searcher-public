# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------

# Polygon [MATIC] on ETH network.

from web3 import Web3


# Connect to Polygon RPC
polygon_rpc = "https://polygon-rpc.com/"
web3 = Web3(Web3.HTTPProvider(polygon_rpc))

# Check if connection is successful
if web3.is_connected():
    pass
else:
    # print("Failed to connect to Polygon network")
    pass

# Function to get the balance of an address
def fetch_from_polygon_rpc(address):
    try:
        # Convert the address to a checksum address
        checksum_address = web3.to_checksum_address(address)
        
        # Get balance in Wei (1 Matic = 10^18 Wei)
        balance_wei = web3.eth.get_balance(checksum_address)
        # Convert Wei to MATIC
        balance_matic = web3.from_wei(balance_wei, 'ether')
        return float(balance_matic)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def fetch_polygon_balance(address):
    '''Entry function'''
    try:
        balance_matic = fetch_from_polygon_rpc(address)
        if balance_matic is not None:
            return 'PolygonRPC', balance_matic
        else:
            pass
    except Exception as e:
        pass
    
    return None, None  # Return None if the request fails


if __name__ == "__main__":
    # Example usage
    polygon_address = "0x12B1545169aD72dA1605d214d5Ed1C456831A0F5"
    bal = fetch_polygon_balance(polygon_address)
    print(bal)