import decimal

WEI = 'wei'
GWEI = 'Gwei'
ETH = 'eth'

FACTORS = {
    WEI: 0,
    GWEI: 9,
    ETH: 18
}

BLOCK_TAG_PENDING = 'pending'
BLOCK_TAG_LATEST = 'latest'
BLOCK_TAG_EARLIEST = 'earliest'


def to_wei(val, unit=ETH) -> str:
    fl = isinstance(val, float)
    if fl and unit == WEI:
        raise ValueError('not allowed float value in WEI')

    val = decimal.Decimal(str(val)) if fl else val
    return str(int(val * pow(10, FACTORS[unit])))


def from_wei(val, to_unit=ETH) -> str:
    if isinstance(val, float):
        raise ValueError('not allowed float value in WEI')

    values = decimal.Decimal(str(val)) / pow(10, FACTORS[to_unit])
    return format(values, '>.18f')


if __name__ == '__main__':
    print(int(0xde0b6b3a7640000))
    print(to_wei(.000054))
    print(to_wei(2.000054))
    print(to_wei(12))

    print(to_wei(.0054, GWEI))
    print(to_wei(122.0054, GWEI))
    print(to_wei(765, GWEI))

    print(to_wei(12123, WEI))

    print('-------------------------')

    print(from_wei(192, WEI))
    print(from_wei(192, GWEI))
    print(from_wei(192, ETH))
    print(from_wei(0xde0b6b3a7640000, ETH))

    args = [0x79cb31, 0x9502f909, 0x5208]
    for a in args:
        print(from_wei(a, ETH))
