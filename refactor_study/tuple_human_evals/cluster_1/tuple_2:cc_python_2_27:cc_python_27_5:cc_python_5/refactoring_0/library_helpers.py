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
def factorize(n):
    """
    Return a dict of prime→exponent for n.
    """
    from math import isqrt
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

def residual_after_factors(n, primes):
    """
    Remove all occurrences of primes from n, return the residual.
    """
    for p in primes:
        while n % p == 0:
            n //= p
    return n

def get_divisors(n):
    """
    Enumerate all divisors of n in O(√n), returning them in ascending order.
    """
    small, large = [], []
    from math import isqrt
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

def is_power_of_two(n):
    """Check if n is a power of two."""
    return n > 0 and (n & (n - 1)) == 0

def count_shift_ops(k):
    """
    Given k = log2(ratio), return minimum ops using shifts of 3,2,1 bits.
    """
    ops = k // 3
    k %= 3
    ops += k // 2
    k %= 2
    ops += k
    return ops
