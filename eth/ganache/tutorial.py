
import ethereum
from ether import *
from config import conf

conf.set_network('ganache')
acc1 = '0xE3899e1c3020f63eC1Da9F1A6a0049Aed80FbC72'
g_acc1 = '0x607A7152A374ADf5B5F8244617AF199F78623832'


def self_account():
    balance = ethereum.get_balance(acc1)
    print(from_wei(balance, ETH))


def transfer():
    value = to_wei(2, ETH)
    tx = ethereum.create_tx(int(value), g_acc1, acc1)
    tx_hash = ethereum.send_tx(tx)
    tx['hash'] = tx_hash
    # tx_hash = ethereum.send_raw_tx('0x42d122a3c8a97751b462e716f194535b37b6f9c8d850ff1ee4747db6dd3760dd')
    [print(k, tx[k]) for k in tx]


def browse_tx():
    tx_hash = ''
    tx = ethereum.get_tx(tx_hash=tx_hash)
    [print(k, tx[k]) for k in tx]


if __name__ == '__main__':
    # self_account()
    transfer()
    # browse_tx()
