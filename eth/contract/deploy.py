from solcx import install_solc, compile_source


def install_compile():
    install_solc(version='latest')  # using CLI could be better


def read_sol(sol_file: str) -> str:
    with open('ShrimpCoin.sol', 'r', encoding='utf-8') as f:
        codes = ''.join(f.readlines())
    return codes


def compile_sol(sol_file: str = 'ShrimpCoin.sol'):
    codes = read_sol(sol_file)
    compiled_sol = compile_source(codes, output_values=['abi', 'bin'])
    contract_id, contract_interface = compiled_sol.popitem()
    abi, bytecode = contract_interface['abi'], contract_interface['bin']
    # TODO deploy to ganache


if __name__ == '__main__':
    # install_compile()
    compile_sol()
