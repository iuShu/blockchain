import decimal

from web3 import Web3, HTTPProvider
from hexbytes import HexBytes
from config import conf

acc = '0xE3899e1c3020f63eC1Da9F1A6a0049Aed80FbC72'


def prepare() -> Web3:
    provider = HTTPProvider(endpoint_uri=conf.cur_network['url'])
    w3 = Web3(provider=provider)
    if w3.isConnected():
        return w3
    raise RuntimeError('prepare web3 instance error')


def print_dict(adict):
    for k, v in adict.items():
        print(k, v.hex() if isinstance(v, HexBytes) else v)


def print_fee(adict):
    gas_price = adict['gasPrice']
    max_fee, pro_fee = adict['maxFeePerGas'], adict['maxPriorityFeePerGas']

    w3 = prepare()
    d = dict()
    d['from'] = adict['from']
    d['to'] = adict['to']
    d['value'] = adict['value']
    d['nonce'] = adict['nonce']
    gas = w3.eth.estimate_gas(d)

    print('gas', Web3.fromWei(gas, 'gwei'))
    print('gasPrice', Web3.fromWei(gas_price, 'gwei'))
    print('tx fee', Web3.fromWei(gas * gas_price, 'ether'))
    print('max fee', Web3.fromWei(max_fee, 'gwei'))
    print('pro fee', Web3.fromWei(pro_fee, 'gwei'))
    print('prd max', calc_max_fee(pro_fee))


def calc_max_fee(priority_fee: int) -> int:
    max_fee = decimal.Decimal('1.01') * decimal.Decimal(str(priority_fee))
    return max_fee.__int__()


def check_balance():
    w3 = prepare()
    balance = w3.eth.get_balance(acc, 'latest')
    print(w3.fromWei(balance, 'ether'), 'ether')


def check_block():
    w3 = prepare()
    block_hash = HexBytes('0x091403e890bbb9577e7d87bc44d38fc851725a5e0a87dca03ef0846ea4d40c80')
    # block = w3.eth.get_block(block_hash)  # web3.datastructures.AttributeDict
    block = w3.eth.get_block(14514212)
    print_dict(block)


def check_tx():
    w3 = prepare()
    # block = HexBytes('0xdd117e5599274f6cfab399095432c49d6ecce5ad8bae81447c7a49f5fb8e38e0')
    # tx = w3.eth.get_transaction_by_block(block, 1)   # web3.datastructures.AttributeDict
    # tx = w3.eth.get_transaction(HexBytes('0xd82fd4aba6571384199c2a81eaeccaafe9f459ba8f2f73c51014b26424c65024'))
    # tx = w3.eth.get_transaction(HexBytes('0x97119a46b0700a9d0886b76488716e1152b60db6e25f12ecdc3bf97a7c701c88'))
    tx = w3.eth.get_transaction(HexBytes('0x35e7d57261022ac76ff3b0eb161afea3da7e0ace048a246bd0e66d016a6f64a5'))
    # tx = w3.eth.get_transaction_by_block(14514212, 5)
    print_dict(tx)
    print()
    print_fee(tx)


def fee_history(calc=False) -> int:
    w3 = prepare()
    if not calc:
        return w3.eth.max_priority_fee

    # calculation details derived from the implementation of web3py
    fh = w3.eth.fee_history(10, 'latest', [5.0])
    # print_dict(fh)
    non_empty_block_fees = [fee[0] for fee in fh['reward'] if fee[0] != 0]
    # print(non_empty_block_fees)
    divisor = len(non_empty_block_fees) if len(non_empty_block_fees) != 0 else 1
    priority_fee_average_for_percentile = round(sum(non_empty_block_fees) / divisor)
    # print(priority_fee_average_for_percentile)
    return priority_fee_average_for_percentile


def send_tx():
    w3 = prepare()
    tx = {
        'from': conf.account('billionaire'),
        'to': conf.account('billionaire2'),
        'value': w3.toWei(.03, 'ether'),
        # 'maxFeePerGas': w3.toWei(250, 'gwei'),
        # 'maxPriorityFeePerGas': w3.toWei(9, 'gwei')
    }
    tx_hash = w3.eth.send_transaction(tx)
    print(tx_hash.hex())
    if tx_hash:
        ptx = w3.eth.get_transaction(tx_hash)
        print_dict(ptx)


def send_raw_tx():
    w3 = prepare()
    account = w3.eth.account
    tx = {
        'chainId': w3.eth.chain_id,
        'from': conf.account('billionaire'),
        'to': conf.account('billionaire2'),
        'value': w3.toWei(.02, 'ether'),
        'nonce': w3.eth.get_transaction_count(conf.account('billionaire'), 'latest'),
        'maxPriorityFeePerGas': fee_history()
    }
    tx['maxFeePerGas'] = calc_max_fee(tx['maxPriorityFeePerGas'])
    tx['gas'] = w3.eth.estimate_gas(tx, 'latest')
    print_dict(tx)

    signed_tx = account.signTransaction(tx, conf.secret('billionaire'))
    print('pending hash', signed_tx.hash.hex())
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    if tx_hash:
        ptx = w3.eth.get_transaction(tx_hash)
        print_dict(ptx)


def filter_logs():
    # web._utils.filters.Filter
    w3 = prepare()
    flt = w3.eth.filter({'fromBlock': 0, 'toBlock': 'latest'})
    # flt = w3.eth.filter('latest')
    # flt = w3.eth.filter('pending')
    logs = w3.eth.get_filter_logs(flt.filter_id)
    changes = w3.eth.get_filter_changes(flt.filter_id)
    print(logs)
    print(changes)
    print(w3.eth.uninstall_filter(flt.filter_id))


if __name__ == '__main__':
    # conf.set_network('mainnet')
    # check_balance()
    # check_block()
    # check_tx()
    # fee_history()
    # send_tx()
    # send_raw_tx()
    # filter_logs()

    pass
