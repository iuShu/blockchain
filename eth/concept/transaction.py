"""
    common fields
        type                the tx type, as of the Berlin version of the protocol, there are two tx types:
                            0(legacy) and 1(EIP-2930), there are two subtypes of txs, those which result in
                            message calls and those which result in the creation of new accounts with associated
                            code (known informally as 'contract creation')
        nonce               a scalar value equal to the number of txs sent by the sender
        gas                 also known as gas limit/units, can be obtained by estimate_gas(tx), different gas fees
                            between different transaction.
        gas price           can be obtained by gas_price(), equals to current max_priority_fee + block.base_fee.
        chainId             the chain id that the tx belongs to.
        input               the data field, described how to call a smart contract.
        access list         ... ...
        r                   corresponding to the signature of the tx and used to determine the sender of the tx.
        s                   corresponding to the signature of the tx and used to determine the sender of the tx.
        v                   ... ...

    contract creation tx
        init                a contract creation tx contains this field.
        data                an unlimited size byte array specifying the input data of the message call.

    legacy tx
        w                   a scalar value encoding Y parity and possibly chain id

    EIP-2930 tx
        type                1
        accessList          list of access entries to warm up, each access list entry is a tuple of an account
                            address and a list of storage keys.
        chainId             equal to the network chain id.
        yParity             signature Y parity.

    EIP-1559 tx
        type                    2
        maxFeePerGas            see the following London Upgrade field 'max fee'
        maxPriorityFeePerGas    see the following London Upgrade field 'priority fee'

    London Upgrade
        base fee        every block has a base fee which acts a reserve price, to be eligible
                        for inclusion in a block the offered price per gas must at least equal
                        the base fee.
        burned fee      the base fee per gas will be 'burned' when the block is mined
                        it equals to base fee * gas limit/units.
        priority fee    the fee incentive miners to include a tx in the block, for transactions that need
                        to get preferentially executed ahead of other transactions in the same block,
                        a higher tip will be necessary to attempt to outbid competing transactions.
        tx fee          the total fee about a tx, equals to gas limit/units * (priority fee + base fee).
        max fee         to execute a transaction on the network, users can specify a maximum limit
                        they are willing to pay for their transaction to be executed. This optional
                        parameter is known as the maxFeePerGas, for a transaction to be executed,
                        the max fee must exceed the sum of the base fee and the tip, the transaction
                        sender is refunded the difference between the max fee and the sum of the base fee
                        and tip, the refund equals to max fee - tx fee.

    interfaces
        eth_sendTransaction         used for sending unsigned txs, which means the node you are sending to
                                    must manage your private key so it can sign the tx and then broadcasting it.
        eth_sendRawTransaction      used to broadcast the txs that have already been signed.

"""

import ethereum
from ethereum import int16, conf, BLOCK_TAG_LATEST, request, to_wei, GWEI
import utils


class Transaction(object):

    def __init__(self):
        self.type = '0x2'                   # 2
        self.transaction_index = '0x2c'     # 24
        self.hash = '0xe1a87f22f7945f533f91ea9a03dd5aa7d9b10f6017e043fd7824d48e6366455a'

        self.block_number = '0xb93e22'      # 12140066
        self.block_hash = '0xdd117e5599274f6cfab399095432c49d6ecce5ad8bae81447c7a49f5fb8e38e0'

        self._from = '0xa500b2427458d12ef70dd7b1e031ef99d1cc09f7'
        self._to = '0x02c2ff931d8624c91844c01bb03e17f416fd021b'
        self.value = '0x2386f26fc10000'     # 10000000000000000 wei = 0.01 eth
        self.nonce = '0xaa60'               # 43616

        self.gas = '0x5208'                             # 21000 (gas limit/units)
        self.gas_price = '0x9502f909'                   # 2500000009 = tx.max_priority_fee + block.base_fee
        self.max_fee_per_gas = '0x9502f9fe'             # 2500000254
        self.max_priority_fee_per_gas = '0x9502f900'    # 2500000000

        self.chain_id = '0x3'
        self.input = '0x'
        self.access_list = []

        self._r = '0x11cff80d908420c299f61c89c59472640a9af93960a71f2165bab1d442ec612f'
        self._s = '0x38a91f554517f182468ba505cd17cc99718dcae18481a9fa57eec4a28c71eab9'
        self._v = '0x1'

        self.tx = self.formal_dict()

    def calc_gas_price(self, base_fee: str) -> int:
        return int16(self.max_priority_fee_per_gas) + int16(base_fee)

    def calc_tx_fee(self) -> int:
        return int16(self.gas) * int16(self.gas_price)

    def calc_tx_max_fee(self) -> int:
        return int16(self.gas) * int16(self.max_fee_per_gas)

    def calc_burnt(self, base_fee: str) -> int:  # London Upgrade burnt fee
        return int16(self.gas) * int16(base_fee)

    def calc_refund(self) -> int:    # tx savings
        return self.calc_tx_max_fee() - self.calc_tx_fee()

    def formal_dict(self) -> dict:
        d = self.__dict__.copy()
        d['from'] = d['_from']
        d['to'] = d['_to']
        d['r'] = d['_r']
        d['s'] = d['_s']
        d['v'] = d['_v']
        d.pop('_from')
        d.pop('_to')
        d.pop('_r')
        d.pop('_s')
        d.pop('_v')
        for k in list(d.keys()):
            nk = utils.to_camel(k)
            d[nk] = d[k]
            if nk != k:
                d.pop(k)
        return d


if __name__ == '__main__':
    # print(int(0x2386f26fc10000))
    # tx = Transaction()
    # print(tx.calc_gas_price(base_fee='0x9'))
    # print(tx.calc_tx_fee())
    # print(tx.calc_tx_max_fee())
    # print(tx.calc_refund())
    # print(tx.calc_burnt(base_fee='0x9'))
    pass
