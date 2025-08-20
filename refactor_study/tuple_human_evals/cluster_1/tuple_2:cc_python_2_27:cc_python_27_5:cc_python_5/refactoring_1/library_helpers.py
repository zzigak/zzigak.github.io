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

def get_divisors(n):
    """
    Enumerate all divisors of n in O(√n), returning them in ascending order.
    """
    small, large = [], []
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
    """
    result = 1
    base %= mod
    while exp:
        if exp & 1:
            result = result * base % mod
        base = base * base % mod
        exp >>= 1
    return result

def min_shift_operations(a, b):
    """
    Return the minimum number of multiply/divide-by-{2,4,8} ops to go
    from a to b, or -1 if impossible.
    """
    if a == b:
        return 0
    if a < b:
        a, b = b, a
    if a % b != 0:
        return -1
    x = a // b
    # must be a power of two
    if x & (x - 1) != 0:
        return -1
    d = x.bit_length() - 1
    ops = d // 3
    d %= 3
    ops += d // 2
    d %= 2
    ops += d
    return ops
