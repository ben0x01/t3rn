import asyncio

from web3 import Web3
from web3.exceptions import TransactionNotFound

from modules.helper import get_estimate_gas, return_hex_value, data_maker

class Bridge:
    def __init__(self, private_key, rpc_url, explorer_url, from_chain, to_chain, to_address, amount):
        self.private_key = private_key
        self.amount = amount
        self.url = "https://pricer.t1rn.io/estimate"
        self.rpc_url = rpc_url
        self.explorer_url = explorer_url
        self.from_chain = from_chain
        self.to_chain = to_chain
        self.to_address = to_address
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.chain_id = self.w3.eth.chain_id
        self.wallet = self.w3.eth.account.from_key(self.private_key)
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en,ru;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Host": "pricer.t1rn.io",
            "Origin": "https://bridge.t1rn.io",
            "Referer": "https://bridge.t1rn.io/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
        }

    async def is_transaction_successful(self, tx_hash: hex) -> bool:
        await asyncio.sleep(30)
        try:
            receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            return receipt['status'] == 1
        except TransactionNotFound:
            print(f"Transaction with hash {tx_hash} not found.")
            return False
        except Exception as e:
            print(f"Error checking transaction: {e}")
            return False

    async def prepare_tx(self, route):
        nonce = self.w3.eth.get_transaction_count(self.wallet.address)
        base_fee = self.w3.eth.gas_price
        max_priority_fee_per_gas = self.w3.eth.max_priority_fee

        estimated_gas_hex = await get_estimate_gas(self.url, self.headers, self.amount, self.from_chain, self.to_chain)
        if not estimated_gas_hex:
            raise ValueError("Estimated gas returned None")
        print(f"Estimated gas (hex): {estimated_gas_hex}")

        data = data_maker(route, return_hex_value(self.amount), estimated_gas_hex[2:], self.wallet.address)
        if not data:
            raise ValueError("data_maker returned None")

        tx = {
            "from": self.wallet.address,
            "to": Web3.to_checksum_address(self.to_address),
            "data": data,
            "value": self.amount,
            "maxPriorityFeePerGas": max_priority_fee_per_gas,
            "maxFeePerGas": base_fee + max_priority_fee_per_gas,
            "nonce": nonce,
            "chainId": self.chain_id,
        }

        estimated_gas = self.w3.eth.estimate_gas(tx)
        tx['gas'] = estimated_gas

        signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
        print("Transaction successfully signed")

        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        if await self.is_transaction_successful(tx_hash):
            print(f'Transaction hash: {self.explorer_url}0x{tx_hash.hex()}')
