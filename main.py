import asyncio

from modules.helper import get_random_network_data_new, get_balance
from modules.bridge import Bridge
from constans import NETWORK_CONFIG, PRIVATE_KEYS_PATH
from modules.helper import load_private_key_from_file


async def start_bridge(private_key):
    random_data = get_random_network_data_new(NETWORK_CONFIG)

    bridge = Bridge(
        private_key,
        random_data["rpc_url"],
        random_data["explorer_url"],
        random_data["chain_identifier_from"],
        random_data["chain_identifier_to"],
        random_data["from_contract_address"],
        get_balance(random_data["rpc_url"], private_key)
    )
    await bridge.prepare_tx(route=random_data["to_contract_address"])


if __name__ == "__main__":
    private_key = load_private_key_from_file(PRIVATE_KEYS_PATH)

    try:
        asyncio.run(start_bridge(private_key))
    except RuntimeError as e:
        print(f"Runtime error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
