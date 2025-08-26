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
def extract_factors(n, primes):
    counts = {}
    for p in primes:
        cnt = 0
        while n % p == 0:
            n //= p
            cnt += 1
        counts[p] = cnt
    return counts, n

def pow2_exp(n):
    if n > 0 and n & (n-1) == 0:
        return n.bit_length() - 1
    return None

def count_shifts(k):
    c = k // 3
    k %= 3
    c += k // 2
    k %= 2
    c += k
    return c


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_27:cc_python_27 ##########

from codebank import *

MOD = 10**9 + 7

def main():
    n = int(input().strip())
    arr = map(int, input().split())
    count = {}
    for num in arr:
        for d in get_divisors(num):
            count[d] = count.get(d, 0) + 1
    maxk = max(count.keys())
    freq = {d: (pow_mod(2, c, MOD) - 1) % MOD for d, c in count.items()}
    for d in sorted(count.keys(), reverse=True):
        for m in range(d*2, maxk+1, d):
            if m in freq:
                freq[d] = (freq[d] - freq[m]) % MOD
    print(freq.get(1, 0))

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_2:cc_python_2 ##########

from codebank import *

PRIMES = [2, 3, 5]

def main():
    a, b = map(int, input().split())
    if a == b:
        print(0)
        return
    counts_a, res_a = extract_factors(a, PRIMES)
    counts_b, res_b = extract_factors(b, PRIMES)
    if res_a != res_b:
        print(-1)
    else:
        ops = sum(abs(counts_a[p] - counts_b[p]) for p in PRIMES)
        print(ops)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_5:cc_python_5 ##########

from codebank import *

def main():
    t = int(input())
    for _ in range(t):
        a, b = map(int, input().split())
        if a == b:
            print(0)
            continue
        lo, hi = min(a, b), max(a, b)
        if hi % lo != 0:
            print(-1)
            continue
        ratio = hi // lo
        e = pow2_exp(ratio)
        if e is None:
            print(-1)
        else:
            print(count_shifts(e))

if __name__ == "__main__":
    main()
