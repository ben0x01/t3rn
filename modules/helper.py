import random
import httpx

from web3 import Web3
from decimal import Decimal

from constans import AMOUNT_IN_WEI, NETWORK_CONFIG


def return_hex_value(amount_wei):
    eth_value = amount_wei / AMOUNT_IN_WEI

    wei_value = Web3.to_wei(eth_value, 'ether')

    hex_value = hex(wei_value)

    print(f"Value in Wei: {wei_value} Wei")
    print(f"Value in Hex: {hex_value}")
    return hex_value[2:]


# amount > 0.005
def data_maker(rooute, amount: str, amount_without_fee, wallet_address):
    data = rooute + "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000" + wallet_address[
                                                                                                                                                                          2:] + "00000000000000000000000000000000000000000000000000" + amount_without_fee + "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000" + amount
    print("DATA TO SEND -", data)
    return data


async def get_estimate_gas(url, headers, amount, from_network, to_network):
    payload = {
        "fromAsset": "eth",
        "toAsset": "eth",
        "fromChain": f"{from_network}",
        "toChain": f"{to_network}",
        "amountWei": f"{amount}",
        "executorTipUSD": 0,
        "overpayOptionPercentage": 0,
        "spreadOptionPercentage": 0
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            response_data = response.json()
            estimated_fee_hex = response_data.get("estimatedReceivedAmountWei", {}).get("hex")
            if estimated_fee_hex:
                print(f"Response: {estimated_fee_hex}")
                return estimated_fee_hex
            else:
                raise ValueError("No 'estimatedReceivedAmountWei' found in the response.")
        else:
            raise httpx.HTTPStatusError(f"Request failed with status code: {response.status_code}",
                                        request=response.request, response=response)


def get_random_network_data_new(my_dict=None):
    if my_dict is None:
        my_dict = NETWORK_CONFIG

    random_network_from = random.choice(list(my_dict.keys()))
    print(f"Bridge from {random_network_from}")

    network_data_from = my_dict[random_network_from]

    if "ROUTES" in network_data_from:
        random_route_key = random.choice(list(network_data_from["ROUTES"].keys()))
        random_route_value = network_data_from["ROUTES"][random_route_key]

        to_network_key = random_route_key.split("_")[1].upper()

        if to_network_key in my_dict:
            chain_identifier_to = my_dict[to_network_key]["CHAIN_IDENTIFIER"]
        else:
            chain_identifier_to = "Unknown"

        print(f"Bridge to {random_route_key}")

        return {
            "from_network": random_network_from,
            "from_contract_address": network_data_from["FROM_CONTRACT_ADDRESS"],
            "to_network_key": random_route_key,
            "to_contract_address": random_route_value,
            "rpc_url": network_data_from["RPC_URL"],
            "explorer_url": network_data_from["EXPLORER_URL"],
            "chain_identifier_from": network_data_from.get("CHAIN_IDENTIFIER"),
            "chain_identifier_to": chain_identifier_to
        }

    remaining_keys = [key for key in my_dict.keys() if key != random_network_from]
    if not remaining_keys:
        return None, None

    random_key = random.choice(remaining_keys)
    print(f"Bridge to {random_key}")

    return {
        "network": random_network_from,
        "random_value": my_dict[random_key],
        "chain_identifier": None
    }


def load_private_key_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            private_key = file.read().strip()
            if not private_key:
                raise ValueError("Private key file is empty")
            return private_key
    except FileNotFoundError:
        raise FileNotFoundError(f"Private key file '{file_path}' not found.")
    except Exception as e:
        raise RuntimeError(f"Error loading private key: {e}")


def get_balance(rpc, private_key):
    w3 = Web3(Web3.HTTPProvider(rpc))
    wallet_address = w3.eth.account.from_key(private_key).address
    balance = w3.eth.get_balance(wallet_address)
    balance_in_ether = Decimal(w3.from_wei(balance, 'ether'))
    normal_balance = float(balance_in_ether)
    rounded_balance = round(normal_balance / 10, 2)
    print(f"Balance after division: {rounded_balance} Ether")
    print(f"Balance in wei after division: {Web3.to_wei(rounded_balance, 'ether')}")
    return Web3.to_wei(rounded_balance, "ether")

