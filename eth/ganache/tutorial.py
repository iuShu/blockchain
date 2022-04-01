import ethereum
from ether import *
from config import conf

conf.set_network('ganache')
acc1 = '0xE3899e1c3020f63eC1Da9F1A6a0049Aed80FbC72'
g_acc1 = '0x41a1A822b13DcD0E61463d9C0f8C9BbbFBd6CAB3'


def self_account():
    balance = ethereum.get_balance(acc1)
    print(from_wei(balance, ETH))


def transfer():
    value = to_wei(0.3, ETH)
    # tx = ethereum.create_tx(int(value), g_acc1, acc1)
    tx_hash = ethereum.send_tx({'from': g_acc1, 'to': acc1, 'value': hex(int(value))})
    # tx['hash'] = tx_hash
    # tx_hash = ethereum.send_raw_tx('0x42d122a3c8a97751b462e716f194535b37b6f9c8d850ff1ee4747db6dd3760dd')
    # [print(k, tx[k]) for k in tx]
    print(tx_hash)


def browse_block(block: str):
    block = '0xd6b333bafeb2fe1e47b297dd33dd70d199c84dc170a7e954499772063186d8b3'
    blk = ethereum.get_block(block)
    [print(k, blk[k]) for k in blk]


def local_sign():
    from eth_account import Account
    from concept.transaction import Transaction
    prv_key = '0xd97becf0e077342ff1ba11c091db79def2ab63b850f41fb8d21ee980c6330677'
    tx = Transaction.create_legacy(g_acc1, acc1, hex(int(to_wei(1, ETH))))
    Transaction.print_tx(tx)
    signed_tx = Account.signTransaction(tx, prv_key)
    tx_hash_hex = signed_tx.rawTransaction.hex()
    print(tx_hash_hex)
    print(ethereum.send_raw_tx(tx_hash_hex))


def check_sign():
    from eth_account import Account
    tx = dict({'from': '0x41a1A822b13DcD0E61463d9C0f8C9BbbFBd6CAB3',
               'to': '0xE3899e1c3020f63eC1Da9F1A6a0049Aed80FbC72',
               'value': '0xde0b6b3a7640000', 'gasPrice': '0x4a817c800', 'gas': '0x5208', 'nonce': '0x3'})
    prv_key = '0xd97becf0e077342ff1ba11c091db79def2ab63b850f41fb8d21ee980c6330677'
    tx_hash_hex = '0x29d018f9da5f5d4bb58dcee96c33963d848288036efb19a2661bc725667775ce'
    signed_tx = Account.signTransaction(tx, prv_key)
    print(signed_tx.rawTransaction.hex())
    print(signed_tx.hash.hex())
    print(signed_tx.hash.hex() == tx_hash_hex)


if __name__ == '__main__':
    # self_account()
    # transfer()
    # browse_tx()
    # browse_block('')
    local_sign()
    # check_sign()


