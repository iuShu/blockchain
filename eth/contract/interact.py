import json
import time

from hexbytes import HexBytes
from ganache.ethapi import conf, prepare, print_dict, calc_max_fee
from deploy import output_abi, contract_addr


def contract_function():
    # contract_json = json.load(fp=open('build/gabi', 'r'))
    # abi = contract_json['abi']
    abi = json.load(fp=open(output_abi, 'r'))
    with open(contract_addr(), 'r') as f:
        address = f.read()

    w3 = prepare()
    contract = w3.eth.contract(abi=abi, address=HexBytes(address))

    for cf in contract.all_functions():
        print('func', cf.function_identifier)

    # balance = contract.functions.balanceOf(w3.eth.accounts[1]).call()
    # print(balance)

    # tx_hash = contract.functions.transfer(w3.eth.accounts[1], 99990001).transact({'from': w3.eth.accounts[0]})
    # receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    # print('transact success', receipt.transactionHash.hex())
    # assert receipt.status == 1  # confirm tx status


def contract_call():
    abi = json.load(fp=open(output_abi, 'r'))
    with open(contract_addr(), 'r') as f:
        address = f.read()

    w3 = prepare()
    acc, acc2 = w3.eth.accounts[0], w3.eth.accounts[1]
    # acc, acc2 = conf.account('billionaire'), conf.account('billionaire2')
    contract = w3.eth.contract(address=HexBytes(address), abi=abi)
    # print(contract, type(contract))

    val = contract.functions.get_balance(acc).call()
    print(acc, 'balance', val)

    val = contract.functions.get_balance(acc2).call()
    print(acc2, 'balance', val)


def contract_transact():
    abi = json.load(fp=open(output_abi))
    with open(contract_addr(), 'r') as f:
        address = f.read()

    w3 = prepare()
    contract = w3.eth.contract(address=HexBytes(address), abi=abi)
    _from, _to, amount = w3.eth.accounts[0], w3.eth.accounts[1], 1112
    tx_hash = contract.functions.transfer(_to, amount).transact({'from': _from})

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print('transact success', receipt.transactionHash.hex())
    assert receipt.status == 1  # confirm tx status


def contract_transact_ropsten():
    abi = json.load(fp=open(output_abi))
    with open(contract_addr(), 'r') as f:
        address = f.read()

    w3 = prepare()
    acc, acc2 = conf.account('billionaire'), conf.account('billionaire2')
    secret = conf.secret('billionaire')
    contract = w3.eth.contract(address=HexBytes(address), abi=abi)
    transfer = contract.get_function_by_name('transfer')
    priority_fee = w3.eth.max_priority_fee
    ftx = {
        'from': acc,
        'nonce': w3.eth.get_transaction_count(HexBytes(acc)),
        'maxFeePerGas': calc_max_fee(priority_fee),
        'maxPriorityFeePerGas': priority_fee
    }
    ftx = transfer(HexBytes(acc2), 1000).buildTransaction(ftx)
    ftx['gas'] = w3.eth.estimate_gas(ftx)
    signed_ftx = w3.eth.account.sign_transaction(ftx, secret)
    ftx_hash = w3.eth.send_raw_transaction(signed_ftx.rawTransaction)
    print('pending tx', ftx_hash.hex())

    start = time.time()
    tx_receipt = w3.eth.wait_for_transaction_receipt(ftx_hash)
    print_dict(tx_receipt)
    print('confirm cost', time.time() - start)
    assert tx_receipt.status == 1   # confirm tx status
    print()

    # from web3.logs import WARN
    # event_logs = contract.events.Transfer().processReceipt(txn_receipt=tx_receipt, errors=WARN)
    # [print(el) for el in event_logs]
    # print()

    tx = w3.eth.get_transaction(ftx_hash)
    input_args = contract.decode_function_input(tx.input)
    print(input_args)


def browse_tx():
    from ganache.ethapi import print_dict, print_topics
    w3 = prepare()
    tx_hash = '0x9770b66f89d6d0b1a0c7540ebf6c5f452972d37c80afee66b6297a4861aaa65e'

    # tx = w3.eth.get_transaction(HexBytes(tx_hash))
    # print_dict(tx)

    receipt = w3.eth.get_transaction_receipt(HexBytes(tx_hash))
    print_dict(receipt)


def events():
    abi = json.load(fp=open(output_abi, 'r'))
    contract_address = contract_addr()
    w3 = prepare()
    contract = w3.eth.contract(abi=abi)
    log_filter = contract.events.Transfer.createFilter(fromBlock=0, address=contract_address)
    print('topics', log_filter.filter_params['topics'][0])
    logs = w3.eth.get_filter_logs(log_filter.filter_id)
    for log in logs:
        evt = log_filter.format_entry(log)  # log_filter.log_entry_formatter = get_event_data(..)
        print_dict(evt)


if __name__ == '__main__':
    conf.set_network('ganache')

    # contract_function()
    # contract_call()
    # contract_transact()
    # contract_transact_ropsten()
    # browse_tx()
    events()
