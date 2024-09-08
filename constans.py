AMOUNT_IN_WEI = 1 * 10 ** 18
AMOUNT_IN_GWEI = 1 * 10 ** 9


NETWORK_CONFIG = {
    "ARB": {
        "FROM_CONTRACT_ADDRESS": "0x8D86c3573928CE125f9b2df59918c383aa2B514D",
        "ROUTES": {
            "TO_OP": "0x56591d596f70737",
            "TO_BASE": "0x56591d596273737"
        },
        "RPC_URL": "https://sepolia-rollup.arbitrum.io/rpc",
        "EXPLORER_URL": "https://sepolia.arbiscan.io/tx/",
        "CHAIN_IDENTIFIER": "arbt"
    },
    "OP": {
        "FROM_CONTRACT_ADDRESS": "0xF221750e52aA080835d2957F2Eed0d5d7dDD8C38",
        "ROUTES": {
            "TO_ARB": "0x56591d5961726274",
            "TO_BASE": "0x56591d596273737"
        },
        "RPC_URL": "https://endpoints.omniatech.io/v1/op/sepolia/public",
        "EXPLORER_URL": "https://optimism-sepolia.blockscout.com/tx",
        "CHAIN_IDENTIFIER": "opsp"
    },
    "BASE": {
        "FROM_CONTRACT_ADDRESS": "0x30A0155082629940d4bd9Cd41D6EF90876a0F1b5",
        "ROUTES": {
            "TO_ARB": "0x56591d5961726274",
            "TO_OP": "0x56591d596f70737"
        },
        "RPC_URL": "https://base-sepolia-rpc.publicnode.com",
        "EXPLORER_URL": "https://sepolia.basescan.org/tx/",
        "CHAIN_IDENTIFIER": "bssp"
    }
}
