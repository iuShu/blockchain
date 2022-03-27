
from config import conf
from ether import *
import requests


def request(params, headers=conf.header(), network=conf.network()):
    idx, version = params['id'], params['jsonrpc']
    print('=>', params)

    resp = requests.post(url=network, json=params, headers=headers)
    if resp.status_code != 200:
        raise ConnectionError(f'unexpected status code {resp.status_code}')

    json = resp.json()
    print('<=', json)
    if 'error' in json.keys():
        raise ConnectionError(json['error'])
    if json['id'] != idx or json['jsonrpc'] != version:
        raise ConnectionError(f'mismatched id and jsonrpc before and after request')
    return json['result']


def int16(val: str) -> int:
    return int(val, base=16)


def get_balance(address) -> int:
    jsonapi = conf.jsonapi('eth_getBalance')
    jsonapi['params'] = [address, 'latest']
    return int16(request(jsonapi))


def get_balances(*addresses) -> list:
    pass


def gas_price() -> int:
    jsonapi = conf.jsonapi('eth_gasPrice')
    return int16(request(jsonapi))


def get_transaction(tx_hash: str) -> dict:
    jsonapi = conf.jsonapi('eth_getTransactionByHash')
    jsonapi['params'] = [tx_hash]
    return request(jsonapi)


def estimate_gas() -> int:
    pass


def tx_fee(gas_units: int, base_fee: int) -> int:
    return gas_units * base_fee  # burnt fee


def test():
    # balance = get_balance('0xE3899e1c3020f63eC1Da9F1A6a0049Aed80FbC72')
    # print(balance, WEI)
    # print(from_wei(balance, ETH), ETH)

    # gas = gas_price()
    # print(gas, WEI)
    # print(from_wei(gas, GWEI), GWEI)
    # print(from_wei(gas, ETH), ETH)

    tx_info = get_transaction('0xe1a87f22f7945f533f91ea9a03dd5aa7d9b10f6017e043fd7824d48e6366455a')
    [print(k, tx_info[k]) for k in tx_info.keys()]

    pass


if __name__ == '__main__':
    test()

