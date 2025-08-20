# ==== NEW HELPER FUNCTIONS ====
from math import isqrt

def get_235_info(n):
    """
    Return exponents of 2,3,5 and remaining cofactor for n.
    """
    fac = factorize(n)
    e2 = fac.get(2, 0)
    e3 = fac.get(3, 0)
    e5 = fac.get(5, 0)
    co = n // (2**e2 * 3**e3 * 5**e5)
    return e2, e3, e5, co

def count_divisors(nums):
    """
    Count for each divisor d how many nums are divisible by d.
    """
    from collections import defaultdict
    cnt = defaultdict(int)
    for x in nums:
        for d in get_divisors(x):
            cnt[d] += 1
    return cnt

def mobius_count(counts, mod):
    """
    Given counts[d] = number of elements divisible by d,
    compute number of subsequences with gcd==1 via inclusion-exclusion.
    """
    freq = {}
    maxk = max(counts.keys())
    for d, c in counts.items():
        freq[d] = (pow_mod(2, c, mod) - 1) % mod
    for d in sorted(counts.keys(), reverse=True):
        m = 2*d
        while m <= maxk:
            if m in freq:
                freq[d] = (freq[d] - freq[m]) % mod
            m += d
    return freq.get(1, 0)

def is_power_of_two(n):
    """Return True if n is a power of two."""
    return n > 0 and (n & (n-1)) == 0

def compute_power2_ops(k):
    """
    Given integer k>=0, return minimum number of shifts (by 3,2,1) to sum to k.
    """
    ops = k//3
    k %= 3
    ops += k//2
    k %= 2
    ops += k
    return ops

def min_shifts(a, b):
    """
    Return minimal operations to transform a into b by *2,4,8 or /2,4,8. -1 if impossible.
    """
    if a == b:
        return 0
    big, small = max(a, b), min(a, b)
    if big % small != 0:
        return -1
    ratio = big // small
    if not is_power_of_two(ratio):
        return -1
    k = ratio.bit_length() - 1
    return compute_power2_ops(k)