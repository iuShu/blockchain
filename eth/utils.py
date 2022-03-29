
def to_camel(name: str) -> str:

    seg = name.split('_')
    for i in range(len(seg)):
        if i != 0:
            seg[i] = seg[i].capitalize()
    return ''.join(seg)


if __name__ == '__main__':
    print(to_camel('max_fee_per_gas'))
