# ==== RETRIEVED HELPER FUNCTIONS ====
def comb(n, k, fact):
    # Success rate: 1/1

    if k < 0 or k > n:
        return 0
    return fact[n] // (fact[k] * fact[n - k])

def binomial(n, k, fact, invfact, mod):
    # Success rate: 2/2

    if k < 0 or k > n:
        return 0
    return fact[n] * invfact[k] % mod * invfact[n - k] % mod

def factorials(n):
    # Success rate: 1/1

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i
    return fact

def modinv(a, mod):
    # Success rate: 2/2

    return pow(a % mod, mod - 2, mod)

def geo_sum(r, t, mod):
    # Success rate: 2/2

    r %= mod
    if r == 1:
        return t % mod
    return (pow(r, t, mod) - 1) * modinv(r - 1, mod) % mod

def precompute_factorials(n, mod):
    # Success rate: 3/3

    fact = [1] * (n + 1)
    invfact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % mod
    invfact[n] = pow(fact[n], mod - 2, mod)
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % mod
    return (fact, invfact)


# ==== NEW HELPER FUNCTIONS ====
def precompute_factorials(n, mod):
    fact = [1] * (n + 1)
    invfact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % mod
    invfact[n] = pow(fact[n], mod - 2, mod)
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % mod
    return fact, invfact

def binomial(n, k, fact, invfact, mod):
    if k < 0 or k > n:
        return 0
    return fact[n] * invfact[k] % mod * invfact[n - k] % mod

def binpow(x, y, mod):
    return pow(x, y, mod)

def sum_diff_weighted(a, n, mod):
    a.sort()
    return (sum(a[n:]) - sum(a[:n])) % mod

def product_mod(seq, mod):
    res = 1
    for v in seq:
        res = res * v % mod
    return res

def prefix_sums(lst):
    res = []
    s = 0
    for v in lst:
        s += v
        res.append(s)
    return res

def compute_abd(n):
    from math import log2
    k = int(log2(n))
    a = []
    x = n
    while x > 0:
        a.append(x - x // 2)
        x //= 2
    b = [n // (3 * 2**i) - n // (6 * 2**i) for i in range(k + 1)]
    d = [n // 2**i - n // (3 * 2**i) for i in range(k + 1)]
    return a, b, d, k

def compute_contribution(n, mod, fact2n, a, b, d, k, j):
    e = a[:j] + [d[j]] + b[j:k]
    x = fact2n * product_mod(e, mod) % mod
    f = product_mod(prefix_sums(e), mod)
    while f > 1:
        t = mod // f + 1
        x = x * t % mod
        f = f * t % mod
    return x

def count_max_gcd_perms(n, mod):
    a, b, d, k = compute_abd(n)
    fact2n = product_mod(range(2, n + 1), mod)
    s = k if n < 3 * 2**(k - 1) else 0
    t = 0
    for j in range(s, k + 1):
        t = (t + compute_contribution(n, mod, fact2n, a, b, d, k, j)) % mod
    return t
