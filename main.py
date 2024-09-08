import asyncio

from modules.helper import get_random_network_data_new
from modules.bridge import Bridge
from constans import NETWORK_CONFIG

async def start_bridge():
    random_data = get_random_network_data_new(NETWORK_CONFIG)

    bridge = Bridge(
        "private_keys",
        random_data["rpc_url"],
        random_data["explorer_url"],
        random_data["chain_identifier_from"],
        random_data["chain_identifier_to"],
        random_data["from_contract_address"],
        10000000000000000
    )
    await bridge.prepare_tx(route=random_data["to_contract_address"])
if __name__ == "__main__":
    asyncio.run(start_bridge())