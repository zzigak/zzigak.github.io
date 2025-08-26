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