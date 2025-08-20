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

def extract_exponents_and_residual(n, primes):
    """
    For given n and list of primes, return (exps, residual)
    where exps is dict prime→exponent in n, and residual is n divided by those prime powers.
    """
    fac = factorize(n)
    exps = {p: fac.get(p, 0) for p in primes}
    residual = n
    for p, e in exps.items():
        residual //= p**e
    return exps, residual

def get_divisors(n):
    """
    Enumerate all divisors of n in O(√n), ascending.
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
    Compute (base^exp) % mod in O(log exp).
    """
    res = 1
    base %= mod
    while exp:
        if exp & 1:
            res = res * base % mod
        base = base * base % mod
        exp >>= 1
    return res

def min_ops_for_ratio(ratio):
    """
    If ratio is a power of two, return minimal number of shifts
    by 2,4,8 to achieve it; else return None.
    """
    if ratio <= 0 or (ratio & (ratio - 1)) != 0:
        return None
    exp = ratio.bit_length() - 1
    # greedy: use as many 8-shifts (3 bits) then 4 (2 bits) then 2 (1 bit)
    ops = exp // 3
    exp %= 3
    ops += exp // 2
    exp %= 2
    ops += exp
    return ops
