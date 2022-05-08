from config import conf
from ether import *
import requests

gas_tracker_url = 'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey' \
                  '=YourKey'


def request(params):
    print('-->', params)
    resp = requests.post(url=conf.cur_network['url'], json=params, headers=conf.cur_header)
    if resp.status_code != 200:
        raise ConnectionError(f'unexpected status code {resp.status_code}')

    json = resp.json()
    print('<--', json)

    if isinstance(json, list):      # multi-request
        err, ret = [], []
        for j in json:
            if 'error' in j.keys():
                err.append(j['error'])
            else:
                ret.append(j['result'])
        if err:
            raise ConnectionError(err)
        return ret
    elif 'error' in json.keys():    # single-request
        raise ConnectionError(json['error'])
    return json['result']


def int16(val: str) -> int:
    return int(val, base=16)


def chain_id() -> int:
    jsonapi = conf.jsonapi('eth_chainId')
    return int16(request(jsonapi))


def protocol_version() -> int:
    jsonapi = conf.jsonapi('eth_protocolVersion')
    return int16(request(jsonapi))


def coinbase() -> str:
    jsonapi = conf.jsonapi('eth_coinbase')
    return request(jsonapi)


def syncing():
    jsonapi = conf.jsonapi('eth_syncing')
    return request(jsonapi)


def accounts():
    jsonapi = conf.jsonapi('eth_accounts')
    return request(jsonapi)


def latest_block() -> int:
    jsonapi = conf.jsonapi('eth_blockNumber')
    return int16(request(jsonapi))


def get_work() -> dict:
    jsonapi = conf.jsonapi('eth_getWork')
    return request(jsonapi)


def mining() -> bool:
    jsonapi = conf.jsonapi('eth_mining')
    return request(jsonapi)


def hashrate() -> str:
    jsonapi = conf.jsonapi('eth_hashrate')
    return request(jsonapi)


def get_balance(address: str, block_tag=BLOCK_TAG_LATEST, block_number: str = '') -> int:
    jsonapi = conf.jsonapi('eth_getBalance')
    jsonapi['params'] = [address, block_tag if not block_number else block_number]
    return int16(request(jsonapi))


def get_balances(addresses: list, block_tag=BLOCK_TAG_LATEST, block_number: str = '') -> list:
    jsonapi = conf.jsonapi('eth_getBalance')
    multiple, idx = [], jsonapi['id']
    for i in range(len(addresses)):
        api = jsonapi.copy()
        api['id'] = idx
        api['params'] = [addresses[i], block_tag if not block_number else block_number]
        multiple.append(api)
        idx += 1
    return list(map(int16, request(multiple)))


def get_tx(tx_hash: str) -> dict:
    jsonapi = conf.jsonapi('eth_getTransactionByHash')
    jsonapi['params'] = [tx_hash]
    return request(jsonapi)


def get_txb(block: str, tx_index: str) -> dict:
    method = 'eth_getTransactionByBlockHashAndIndex' if len(block) > 64 else 'eth_getTransactionByBlockNumberAndIndex'
    jsonapi = conf.jsonapi(method)
    jsonapi['params'] = [block, tx_index]
    return request(jsonapi)


def get_tx_receipt(tx_hash: str) -> dict:
    jsonapi = conf.jsonapi('eth_getTransactionReceipt')
    jsonapi['params'] = [tx_hash]
    return request(jsonapi)


def get_block(block: str, hydrated=False) -> dict:
    method = 'eth_getBlockByHash' if len(block) > 64 else 'eth_getBlockByNumber'
    jsonapi = conf.jsonapi(method)
    jsonapi['params'] = [block, hydrated]
    return request(jsonapi)


def get_tx_count(addr: str) -> int:
    jsonapi = conf.jsonapi('eth_getTransactionCount')
    jsonapi['params'] = [addr, BLOCK_TAG_LATEST]
    return int16(request(jsonapi))


def get_txb_count(block: str) -> int:
    method = 'eth_getBlockTransactionCountByHash' if len(block) > 64 else 'eth_getBlockTransactionCountByNumber'
    jsonapi = conf.jsonapi(method)
    jsonapi['params'] = [block]
    return int16(request(jsonapi))


def get_uncle_count(block: str) -> int:
    method = 'eth_getUncleCountByBlockHash' if len(block) > 64 else 'eth_getUncleCountByBlockNumber'
    jsonapi = conf.jsonapi(method)
    jsonapi['params'] = [block]
    return int16(request(jsonapi))


def gas_price() -> int:
    jsonapi = conf.jsonapi('eth_gasPrice')
    return int16(request(jsonapi))


def estimate_gas(tx: dict) -> int:  # also known as 'gas limit/units'
    jsonapi = conf.jsonapi('eth_estimateGas')
    jsonapi['params'] = [tx]
    return int16(request(jsonapi))


def max_priority_fee() -> int:
    # non-spec method and only supported by some clients
    jsonapi = conf.jsonapi('eth_maxPriorityFeePerGas')
    return int16(request(jsonapi))


def gas_tracker():
    # require vpn

    resp = requests.get(url=gas_tracker_url)    # calculated by oracle fee history statistic
    print(resp.status_code)
    json = resp.json()['result']
    print(json)

    conf.set_network('mainnet')
    print(max_priority_fee())                   # provided by ethereum node/client


def sign_tx(tx: dict) -> str:
    # jsonapi = conf.jsonapi('eth_signTransaction')
    # jsonapi['params'] = [tx]
    # return request(jsonapi)
    pass


def send_tx(tx: dict):
    jsonapi = conf.jsonapi('eth_sendTransaction')
    jsonapi['params'] = [tx]
    return request(jsonapi)
    # pass


def send_raw_tx(tx_hash: str):
    jsonapi = conf.jsonapi('eth_sendRawTransaction')
    jsonapi['params'] = [tx_hash]
    return request(jsonapi)


def get_code(addr: str, block_tag=BLOCK_TAG_LATEST, block_number: str = '') -> str:
    jsonapi = conf.jsonapi('eth_getCode')
    jsonapi['params'] = [addr, block_tag if not block_number else block_number]
    return request(jsonapi)


def new_filter() -> str:
    # jsonapi = conf.jsonapi('eth_newFilter')
    # jsonapi['params'] = [{'from': 0, 'to': 'latest', 'address': '0xE3899e1c3020f63eC1Da9F1A6a0049Aed80FbC72'}]
    # return request(jsonapi)
    pass


def new_block_filter() -> str:
    jsonapi = conf.jsonapi('eth_newBlockFilter')
    return request(jsonapi)


def new_pending_tx_filter() -> str:
    jsonapi = conf.jsonapi('eth_newPendingTransactionFilter')
    return request(jsonapi)


def uninstall_filter(*filter_id) -> bool:
    jsonapi = conf.jsonapi('eth_uninstallFilter')
    jsonapi['params'] = list(filter_id)
    return request(jsonapi)


def get_logs():
    jsonapi = conf.jsonapi('eth_getLogs')
    # jsonapi['params'] = ['0xE3899e1c3020f63eC1Da9F1A6a0049Aed80FbC72']
    return request(jsonapi)


def get_filter_logs(filter_id: str) -> list:
    jsonapi = conf.jsonapi('eth_getFilterLogs')
    jsonapi['params'] = [filter_id]
    return request(jsonapi)


def get_filter_changes(filter_id: str) -> list:
    jsonapi = conf.jsonapi('eth_getFilterChanges')
    jsonapi['params'] = [filter_id]
    return request(jsonapi)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def estimate_tx_fee(tx: dict) -> int:
    gas_price_api = conf.jsonapi('eth_gasPrice')
    gas_api = conf.jsonapi('eth_estimateGas')
    gas_api['params'] = [tx]
    jsonapi = [gas_price_api, gas_api]
    res = request(jsonapi)
    return int16(res[0]) * int16(res[1])


def calc_tx_fee(tx: dict) -> int:
    return int16(tx['gas']) * int16(tx['gasPrice'])


def create_tx(value: int, _from: str, _to: str) -> dict:
    tx = {
        'value': str(hex(value)),   # wei
        'from': _from,
        'to': _to,
        'chainId': conf.cur_network['id'],
        # 'input': '0x',
        # 'accessList': [],
        'type': '0x2'
    }
    gas_price_api = conf.jsonapi('eth_gasPrice')
    gas_api = conf.jsonapi('eth_estimateGas')
    gas_api['params'] = [tx]
    nonce_api = conf.jsonapi('eth_getTransactionCount')
    nonce_api['params'] = [_from, BLOCK_TAG_LATEST]
    jsonapi = [gas_price_api, gas_api, nonce_api]
    res = request(jsonapi)
    tx['gasPrice'] = res[0]
    tx['gas'] = res[1]
    nonce = int16(res[2])
    tx['nonce'] = hex(0 if nonce == 0 else (nonce + 1))
    return tx


def test():
    # conf.set_network('mainnet')

    # chainId = chain_id()
    # print(chainId)

    # ver = protocol_version()
    # print(ver)

    # sync = syncing()
    # print(sync)

    # acs = accounts()
    # print(acs)

    # cb = coinbase()
    # print(cb)

    # bn = latest_block()
    # print(bn)

    acc = '0xE3899e1c3020f63eC1Da9F1A6a0049Aed80FbC72'
    # balance = get_balance(acc)
    # print(balance, WEI)
    # print(from_wei(balance, ETH), ETH)

    # balances = get_balances(conf.all_accounts())
    # print(balances)

    # gas = gas_price()
    # print(gas, WEI)
    # print(from_wei(gas, GWEI), GWEI)
    # print(from_wei(gas, ETH), ETH)

    tx_hash = '0xe1a87f22f7945f533f91ea9a03dd5aa7d9b10f6017e043fd7824d48e6366455a'
    # tx_info = get_tx(tx_hash)
    # [print(k, tx_info[k]) for k in tx_info.keys()]

    # [tx_info.pop(k) for k in ['gas', 'gasPrice', 'maxFeePerGas', 'maxPriorityFeePerGas']]
    # eg = estimate_gas(tx_info)
    # print(eg)

    # tx_fee = estimate_tx_fee()
    # print(tx_fee, from_wei(tx_fee, GWEI), from_wei(tx_fee, ETH))

    block_index = '0xb93e22'
    block_hash = '0xdd117e5599274f6cfab399095432c49d6ecce5ad8bae81447c7a49f5fb8e38e0'
    # block = get_block(block_index, True)
    # [print(k, block[k])for k in block.keys()]

    # tx_info = get_txb(block_hash, str(hex(1)))
    # [print(k, tx_info[k]) for k in tx_info.keys()]

    # tx_count = get_tx_count(block_index)
    # print(tx_count)

    # uc_count = get_uncle_count(block_hash)
    # print(uc_count)

    from_addr = '0xcbfb60f6a39e9e5e79f48555de777b9aab19c99a'
    to_addr = '0xc7a97d815770675979c150829232f83112267056'
    # code = get_code(to_addr)
    # print(code)

    # work = get_work()
    # print(work)

    # mine = mining()
    # print(mine)

    # hr = hashrate()
    # print(hr)

    # print(from_wei(10000000000000000, ETH))
    # print(from_wei(21000 * 2500000000, ETH))

    fa = conf.account('billionaire')
    ta = conf.account('billionaire2')
    # tx = create_tx(int(to_wei(0.25, ETH)), fa, ta)
    # [print(k, tx[k]) for k in tx]

    # res = send_raw_tx(tx_hash='')
    # print(res)

    # rtx = get_tx_receipt(tx_hash)
    # [print(k, rtx[k]) for k in rtx]

    # logs = get_logs()
    # print(logs)

    # fid = new_filter()
    # b_fid = new_block_filter()
    # pt_fid = 0 # new_pending_tx_filter()
    # print(fid, b_fid, pt_fid)
    #
    # for i in (fid, b_fid):
    #     filter_logs = get_filter_logs(i)
    #     filter_changes = get_filter_changes(i)
    #     print(filter_logs)
    #     print(filter_changes)
    #
    # print(uninstall_filter(fid, b_fid))

    # conf.set_network('mainnet')
    # pro_fee = max_priority_fee()
    # print(pro_fee)

    gas_tracker()

    pass


if __name__ == '__main__':
    test()

