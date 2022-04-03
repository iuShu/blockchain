"""
    fields
        parentHash      the Keccak 256-bit hash of the parent block's header.
        ommersHash      the Keccak 256-bit hash of the ommers list portion of this block.
        stateRoot       the Keccak 256-bit hash of the root node of the state trie, after all txs are executed
                        and finalisation applied.
        txsRoot         the Keccak 256-bit hash of the root node of the trie structure populated with each tx in
                        the txs list portion of the block.
        receiptsRoot    the Keccak 256-bit hash of the root node of the trie structure populated with the receipts
                        of each tx in the txs list portion of the block.
        logsBloom       the Bloom filter composed from indexable information(log address and log topics) contained
                        in each log entry from the receipt of each tx in the txs list.
        number          a scalar value equal to the number of ancestor blocks, the genesis block has a number of zero.
        gasLimit        a scalar value equal to the current limit of gas expenditure per block.
        gasUsed         a scalar value equal to the total gas used in txs in this block.
        difficulty      a scalar value corresponding to the difficulty level of this block, this can be calculated
                        from the previous block's difficulty level and the timestamp.
        timestamp       a scalar value equal to the reasonable output of the Unix's time() at this block's inception.
        beneficiary     the 160-bit address to which all fees collected from the successful mining of this block.
        extraData       an arbitrary byte array containing data relevant to this block, this must be 32 bytes or fewer.
        mixHash         a 256-bit hash which, combined with the nonce, proves that a sufficient amount of computation
                        has been carried out on this block.
        nonce           a 64-bit value which, combined with the mixHash, proves that a sufficient amount of computation
                        has been carried out in this block.

"""


class Block(object):

    def __init__(self):
        self.number = '0xb93e22'
        self.hash = '0xdd117e5599274f6cfab399095432c49d6ecce5ad8bae81447c7a49f5fb8e38e0'
        self.parent_hash = '0x4318f487864850f04fc2c1f2777c479a2e380748a619a381d35316091e4da1ee'

        self.nonce = '0xc8a1ee2e1482d05a'
        self.mix_hash = '0xab351eeb8b8a32c3b2bac7291fd0d0d6fa1ef7311b0ff02d8a243296d4b63e61'
        self.miner = '0x169d07d5c0703733aa505008e9627577c087eb63'
        self.timestamp = '0x62409a8d'
        self.difficulty = '0x1807e85d9'
        self.total_difficulty = '0x916e3084eb8d4b'

        self.gas_limit = '0x7a1200'     # 8000000
        self.gas_used = '0x79cb31'      # 7981873
        self.base_fee_per_gas = '0x9'   # 9         wei
        self.transactions = []

        self.state_root = ''
        self.receipts_root = ''
        self.transactions_root = ''

        self.uncles = []
        self.sha3_uncles = '0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347'
        self.extra_data = '0x436f696e66617374'
        self.size = '0x6086'

        self.logs_bloom = '0x84008000000000002000a08000000000408000004000000000000082a800100400000880048800000040002' \
                          '004100000201000400206800200000000002042000610100400000000000c1008000010000020000012000000' \
                          '145002088c0020000408082022440a0050000000001108a000220000504000100080001000000110000280040' \
                          '00004060120800040000020208000010041015008400000204000100600260002002008100100200500004000' \
                          '4010000084000040402008000040000400000a000000000000042080200100408200000000000002080000001' \
                          '020020011000000018208000010400008408002006044006810400000890000480000'


if __name__ == '__main__':
    print(int(0x79cb31))
