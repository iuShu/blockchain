from solcx import install_solc, compile_source
from ganache.ethapi import prepare
from config import conf
from hexbytes import HexBytes

acc = '0xE3899e1c3020f63eC1Da9F1A6a0049Aed80FbC72'


def install_compile():
    install_solc(version='latest')  # using CLI could be better


def read_sol(sol_file: str) -> str:
    with open('ShrimpCoin.sol', 'r', encoding='utf-8') as f:
        codes = ''.join(f.readlines())
    return codes


def compile_sol(sol_file: str = 'ShrimpCoin.sol', deploy=False):
    codes = read_sol(sol_file)
    compiled_sol = compile_source(codes, output_values=['abi', 'bin'])
    contract_id, contract_interface = compiled_sol.popitem()
    abi, bytecode = contract_interface['abi'], contract_interface['bin']
    print(abi)
    print('0x' + bytecode)  # the input field in a contract tx

    if not deploy:
        return

    conf.set_network('ganache')
    w3 = prepare()
    w3.eth.default_account = w3.eth.accounts[0]
    shrimp_coin = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = shrimp_coin.constructor().transact()      # deploy by a legacy tx

    print('wait for receipt')
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print('tx receipted by', tx_receipt)
    deployed = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    val = deployed.functions.get_balance(w3.eth.default_account).call()
    print('contract return', val)


def deploy_dynamic_fee(sol_file: str = 'ShrimpCoin.sol', deploy=False):
    from ganache.ethapi import calc_max_fee, print_dict
    codes = read_sol(sol_file)
    compiled_sol = compile_source(codes, output_values=['abi', 'bin'])
    contract_id, contract_interface = compiled_sol.popitem()
    abi, bytecode = contract_interface['abi'], contract_interface['bin']

    if not deploy:
        return

    conf.set_network('ganache')
    w3 = prepare()
    w3.eth.default_account = w3.eth.accounts[0]
    shrimp_coin = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = shrimp_coin.constructor().transact({
        'maxFeePerGas': calc_max_fee(w3.toWei(2, 'gwei')),
        'maxPriorityFeePerGas': w3.toWei(2, 'gwei')  # fetch by api in test/prod network
    })

    print('wait for receipt of', tx_hash.hex())
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)   # = w3.eth.get_tx_receipt(tx_hash)
    print('tx receipted by', tx_receipt.contractAddress)
    contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    val = contract.functions.get_balance(w3.eth.default_account).call()
    print('contract return', val)


def call_contract():
    codes = read_sol('ShrimpCoin.sol')
    compiled_sol = compile_source(codes, output_values=['abi', 'bin'])
    contract_id, contract_interface = compiled_sol.popitem()
    abi = contract_interface['abi']

    conf.set_network('ganache')
    w3 = prepare()
    w3.eth.default_account = w3.eth.accounts[0]
    deployed_address = '0x8fb5D1914090996e0970484b3834cec15cFF71fE'
    deployed_address_v2 = '0x48492CEe25E797Be8bEA1e4241F5B1B499212E34'
    contract = w3.eth.contract(address=HexBytes(deployed_address), abi=abi)
    # print(contract, type(contract))

    # for cf in contract.all_functions():
    #     print(cf.function_identifier)

    val = contract.functions.get_balance(w3.eth.default_account).call()
    print('contract return', val)

    c_func = contract.get_function_by_name('transfer')


def browse_tx():
    from ganache.ethapi import print_dict
    conf.set_network('ganache')
    w3 = prepare()
    contract_tx_hash = HexBytes('0x078d88e8c90f17ed7cfb37237c17e0a390a07a1894d69a1ef9ac2d4cbd65e8e2')
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


if __name__ == '__main__':
    # install_compile()
    # compile_sol()
    deploy_dynamic_fee(deploy=True)
    # call_contract()
    # browse_tx()
    # browser_dynamic_tx()

