import json
import os.path
import time

from solcx import install_solc, compile_source
from ganache.ethapi import prepare, calc_max_fee, print_dict
from config import conf
from hexbytes import HexBytes

output_abi = 'build/abi'
output_bytecode = 'build/bytecode'
output_address = 'build/{network}/address'


def install_compile():
    install_solc(version='latest')  # using CLI could be better


def read_sol(sol_file: str) -> str:
    with open(sol_file, 'r', encoding='utf-8') as f:
        codes = ''.join(f.readlines())
    return codes


def compile_sol(sol_file: str = 'ShrimpCoin.sol'):
    codes = read_sol(sol_file)
    compiled_sol = compile_source(codes, output_values=['abi', 'bin'])
    contract_id, contract_interface = compiled_sol.popitem()
    abi, bytecode = contract_interface['abi'], contract_interface['bin']
    print(abi)
    print('0x' + bytecode)  # the input field in a contract tx

    json.dump(abi, fp=open(output_abi, 'w'))
    with open(output_bytecode, 'w') as f:
        f.write(bytecode)


def deploy():
    abi = json.load(fp=open(output_abi, 'r'))
    with open(output_bytecode, 'r') as f:
        bytecode = f.read()

    w3 = prepare()
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = contract.constructor().transact({'from': w3.eth.accounts[0]})
    print('pending tx', tx_hash.hex())

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print('deployed success', tx_receipt.contractAddress)
    assert tx_receipt.status == 1
    save_deployed_address(tx_receipt.contractAddress)


def deploy_ropsten():
    abi = json.load(fp=open(output_abi, 'r'))
    with open(output_bytecode, 'r') as f:
        bytecode = f.read()

    w3 = prepare()
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    acc, secret = conf.account('billionaire'), conf.secret('billionaire')
    priority_fee = w3.eth.max_priority_fee
    tx = {
        'from': acc,
        'nonce': w3.eth.get_transaction_count(HexBytes(acc)),
        'maxFeePerGas': calc_max_fee(priority_fee),
        'maxPriorityFeePerGas': priority_fee
    }
    ftx = contract.constructor().buildTransaction(tx)
    ftx['gas'] = w3.eth.estimate_gas(ftx)
    signed_ftx = w3.eth.account.sign_transaction(ftx, secret)
    ftx_hash = w3.eth.send_raw_transaction(signed_ftx.rawTransaction)
    print('pending tx', ftx_hash)

    start = time.time()
    tx_receipt = w3.eth.wait_for_transaction_receipt(ftx_hash)   # = w3.eth.get_tx_receipt(tx_hash)
    print('deployed success', tx_receipt.contractAddress)
    print('confirm cost', time.time() - start)
    assert tx_receipt.status == 1
    save_deployed_address(tx_receipt.contractAddress)


def browse_tx():
    from ganache.ethapi import print_dict
    w3 = prepare()
    contract_tx_hash = HexBytes('0x078d88e8c90f17ed7cfb37237c17e0a390a07a1894d69a1ef9ac2d4cbd65e8e2')
    contract_tx_hash = HexBytes('0x7c31e29ba00a48624cc275f0c1297858d976431e5ce9bfc97445c0f5cebd43b8')
    contract_tx_hash = HexBytes('0x7f656f7bea77e39bc6e8419d81ae45d23923cdf052679116b00befb5413b448c')
    tx = w3.eth.get_transaction(contract_tx_hash)
    print_dict(tx)
    print('tx fee', w3.fromWei(tx['gas'] * tx['gasPrice'], 'ether'), 'ether')
    print()

    receipt = w3.eth.get_transaction_receipt(contract_tx_hash)
    for k, v in receipt.items():
        print(k, v.hex() if isinstance(v, HexBytes) else v)


def browser_dynamic_tx():
    from ganache.ethapi import print_dict
    w3 = prepare()
    tx = w3.eth.get_transaction_by_block(12167480, 2)
    print_dict(tx)


def save_deployed_address(contract_address):
    path = contract_addr()
    directory = os.path.split(path)[0]
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(path, 'w') as f:
        f.write(contract_address)


def contract_addr() -> str:
    network = conf.cur_network['name']
    return output_address.replace('{network}', network)


if __name__ == '__main__':
    conf.set_network('ganache')

    # install_compile()
    # compile_sol()
    deploy()
    # deploy_ropsten()
    # browse_tx()
    # browser_dynamic_tx()
    pass

