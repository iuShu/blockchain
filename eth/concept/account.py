"""
    see original doc at https://ethereum.org/en/developers/docs/accounts/

    keypair
        an account is made up of a cryptographic pair of keys: public and private keys.

    types
        externally-owned    controlled by anyone with the private keys.
        contract            a smart contract deployed to the network, controlled by code.

    fields
        nonce           a counter that indicates the number of txs sent from the account,
                        in a contract account, this represents the number of contracts created by the account.
        balance         the number of wei owned by this address.
        codeHash        this hash refers to the code of an account on the EVM, the code gets executed if
                        the account gets a message call, this field cannot be changed, for externally owned
                        accounts, this field is the hash of an empty string.
        storageHash     storage hash, a 256-bit hash of the root node of a Merkle Patricia trie that
                        encodes the storage contents of the account. This trie encodes the hash of
                        the storage contents of this account, and is empty by default.
"""


class Account(object):

    def __init__(self):
        self.nonce = 0
        self.balance = 0
        self.code_hash = '0x0'
        self.storage_root = '0x0'

