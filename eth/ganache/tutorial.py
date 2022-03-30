
import ethereum
from ether import *
from config import conf

conf.set_network('ganache')
acc1 = '0xE3899e1c3020f63eC1Da9F1A6a0049Aed80FbC72'
g_acc1 = '0xB913F99dD138b5bB593466A932be087D57eAcCAF'


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
    tx_hash = '0xc5250e36c0eeb88c99b9d3eabd737f7e86db4040f24243089f8b231cb8f67a84'
    tx = ethereum.get_tx(tx_hash=tx_hash)
    [print(k, tx[k]) for k in tx]


def backup() -> dict:
    init_fields = ['value', 'to', 'from', 'chainId', 'type', 'gas', 'gasPrice', 'nonce']
    signed_tx = {
        'nonce': '0x0',
        'from': '0xb913f99dd138b5bb593466a932be087d57eaccaf',
        'to': '0xe3899e1c3020f63ec1da9f1a6a0049aed80fbc72',
        'value': '0x1bc16d674ec80000',
        'gas': '0x5208',
        'gasPrice': '0x4a817c800',

        'hash': '0xc5250e36c0eeb88c99b9d3eabd737f7e86db4040f24243089f8b231cb8f67a84',
        'blockNumber': '0x1',
        'blockHash': '0x715e0d35971fbfe929e42597d5d56622c0dbf2a02ad25027b085fd2996c37875',
        'transactionIndex': '0x0',
        'input': '0x',
        'v': '0x25',
        'r': '0x2ef9c79237e24b453e275937ef753727490f090a23b8532a0e237b3dc96dfb92',
        's': '0xee6274bae3e130ab90dbd10d8663b884bda07898239eb47f7d3313cb26bdaa5'
    }
    for k in list(signed_tx.keys()):
        if k not in init_fields:
            signed_tx.pop(k)
    return signed_tx


def keccak_test():
    from Crypto.Hash import keccak
    tx = backup()
    # print(tx.__str__())
    k = keccak.new(digest_bits=256)
    k.update(bytes(tx.__str__(), encoding='utf8'))
    hd = k.hexdigest()
    print('0x' + hd)


if __name__ == '__main__':
    # self_account()
    # transfer()
    # browse_tx()
    keccak_test()

