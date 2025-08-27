import math


def get_left_zero_count(num: int) -> int:
    return int(32 - math.ceil(math.log2(num)))


def get_bit_space(num: int) -> int:
    return math.ceil(math.log2(num + 1))


def udiv(value1: int, value2: int) -> int:
    lzc2 = get_left_zero_count(value2) + 32

    v2_sub = value2 * (2**lzc2)
    print(f"got log(x)={math.log2(v2_sub)}")
    v2_add = 2**lzc2
    v1_rem = value1
    v3 = 0

    while v2_sub >= 1:
        if v1_rem >= v2_sub:
            v1_rem -= v2_sub
            v3 += v2_add
        v2_sub = int(v2_sub / 2)
        v2_add = int(v2_add / 2)
    return v3


num_pairs = [
    (1, 2**32 - 1),
    (1, 2**32),
    (2**20, 2**20),
    (2**10 - 1, 2**30 - 1),
    (1234, 7859),
    (1023, 0xFF),
    (1024, 256),
]

for pair in num_pairs:
    product = pair[0] * pair[1]
    print(
        f" got {pair[0]} * {pair[1]}, "
        f"with {get_bit_space(pair[0])} bit * {get_bit_space(pair[1])} bit "
        f"= {get_bit_space(product)} bit",
    )

print(udiv(24949300, 30310))
print(24949300 / 30310)
