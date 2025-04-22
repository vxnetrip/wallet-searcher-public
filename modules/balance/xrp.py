# ----------------------------------------------------------------------------
#                            => CREDITS <=
# ----------------------------------------------------------------------------
#                 HACK: Developed and maintained by VXNET
#             ✦ Best services: https://discord.gg/HmGHGww2kY ✦
#                      Web: http://lefeu.nvnet.pl
# ----------------------------------------------------------------------------

# This script connects to RPC to get address balance.
# This is much better way than using public apis.

import xrpl


def fetch_from_ripple_rpc(address):
    # client = xrpl.clients.JsonRpcClient(
    #     "https://s2.ripple.com:51234/"
    # )

    # Connect to the XRP Ledger mainnet
    client = xrpl.clients.JsonRpcClient("https://s1.ripple.com:51234/")  # Mainnet URL

    # Create an AccountInfo request
    account_info = xrpl.models.requests.AccountInfo(
        account=address,
        ledger_index="validated",
        strict=True
    )

    try:
        # Make the request to the XRP ledger
        response = client.request(account_info)
        result = response.result

        # Check if 'account_data' is present in the response
        if 'account_data' in result:
            balance_in_drops = result['account_data']['Balance']
            balance_in_xrp = float(balance_in_drops) / 1_000_000
            return balance_in_xrp
        else:
            # Handle case where the account doesn't exist or is inactive
            return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def fetch_xrp_balance(address):
    try:
        balance_xrp = fetch_from_ripple_rpc(address)
        if balance_xrp is not None:
            return 'RippleXRP', balance_xrp
        else:
            print("NOT OK")
            pass
    except Exception as e:
        raise e
    
    return None, None  # Return None if the request fails


if __name__ == "__main__":
    res = fetch_xrp_balance("rMtoKCb4ZtS1UU5kD6B6KAKB85vH7JsAKo")
    print(res)