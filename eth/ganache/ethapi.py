from web3 import Web3, HTTPProvider
from config import conf

acc = '0xE3899e1c3020f63eC1Da9F1A6a0049Aed80FbC72'


def prepare() -> Web3:
    conf.set_network('ganache')
    provider = HTTPProvider(endpoint_uri=conf.cur_network['url'])
    w3 = Web3(provider=provider)
    if w3.isConnected():
        return w3
    raise RuntimeError('prepare web3 instance error')


def check_balance():
    w3 = prepare()
    balance = w3.eth.get_balance(acc, 'latest')
    print(w3.fromWei(balance, 'ether'), 'ether')


def send_tx():
    w3 = prepare()
    tx = {
        'from': w3.eth.coinbase,
        'to': acc,
        'value': w3.toWei(.5, 'ether')
    }
    tx_hash = w3.eth.send_transaction(tx)
    print(tx_hash.hex())


def test():
    w3 = prepare()


if __name__ == '__main__':
    # check_balance()
    send_tx()
    # test()
