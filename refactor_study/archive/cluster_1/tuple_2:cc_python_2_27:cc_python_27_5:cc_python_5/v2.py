# ########## LIBRARY HELPERS ##########

# ==== RETRIEVED HELPER FUNCTIONS ====

# Selected Helper Functions

from math import isqrt

def factorize(n):
    """
    Return a dict of prime→exponent for n.
    """
    d = {}
    i = 2
    while i <= isqrt(n):
        while n % i == 0:
            d[i] = d.get(i, 0) + 1
            n //= i
        i += 1 if i == 2 else 2
    if n > 1:
        d[n] = d.get(n, 0) + 1
    return d

# Selected because: The solution plan relies on extracting the exponents of primes 2, 3, and 5
# from each number and checking the remaining cofactor. `factorize` provides exactly the
# prime→exponent mapping needed to compute both the counts for 2,3,5 and to form the
# residual co-prime part for equality checking.


# Selected Helper Functions

def get_divisors(n):
    """
    Enumerate all divisors of n in O(√n), returning them in ascending order.
    Selected because: We need to, for each a_i, list all its divisors to
    increment count[d] for every d | a_i.
    """
    small = []
    large = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            small.append(i)
            if i != n // i:
                large.append(n // i)
        i += 1
    large.reverse()
    return small + large

def pow_mod(base, exp, mod):
    """
    Modular exponentiation: compute (base^exp) % mod in O(log exp).
    Selected because: We need fast computation of 2^count[d] mod M for
    each divisor to count all non-empty subsets.
    """
    result = 1
    base %= mod
    while exp:
        if exp & 1:
            result = result * base % mod
        base = base * base % mod
        exp >>= 1
    return result


# No helper functions selected as the solution uses only direct integer operations:
# - Checking divisibility and power-of-two via bitwise tests
# - Computing the exponent via bit_length()
# - Greedy decomposition with simple arithmetic


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


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_27:cc_python_27 ##########

from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    arr = list(map(int, data[1:]))
    counts = count_divisors(arr)
    mod = 10**9 + 7
    print(mobius_count(counts, mod))

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_2:cc_python_2 ##########

from codebank import *

def main():
    a, b = map(int, input().split())
    e2_a, e3_a, e5_a, cof_a = get_235_info(a)
    e2_b, e3_b, e5_b, cof_b = get_235_info(b)
    if cof_a != cof_b:
        print(-1)
    else:
        print(abs(e2_a - e2_b) + abs(e3_a - e3_b) + abs(e5_a - e5_b))

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_5:cc_python_5 ##########

from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        a = int(data[idx]); b = int(data[idx+1])
        idx += 2
        out.append(str(min_shifts(a, b)))
    print("\n".join(out))

if __name__ == "__main__":
    main()
