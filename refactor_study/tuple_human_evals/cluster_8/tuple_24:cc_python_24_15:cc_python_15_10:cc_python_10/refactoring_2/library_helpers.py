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
def binpow(x, y, mod):
    return pow(x, y, mod)

def modinv(a, mod):
    return pow(a, mod - 2, mod)

def precompute_factorials(n, mod):
    fact = [1] * (n + 1)
    invfact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % mod
    invfact[n] = modinv(fact[n], mod)
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % mod
    return fact, invfact

def nCr(n, k, fact, invfact, mod):
    if k < 0 or k > n:
        return 0
    return fact[n] * invfact[k] % mod * invfact[n - k] % mod

def product_mod(lst, mod):
    res = 1
    for x in lst:
        res = res * x % mod
    return res

def compute_seq_lengths(n):
    a = []
    while n > 0:
        a.append(n - n // 2)
        n //= 2
    return a

def compute_b_d(n, k):
    b = [n // (3 * (1 << i)) - n // (6 * (1 << i)) for i in range(k + 1)]
    d = [n // (1 << i) - n // (3 * (1 << i)) for i in range(k + 1)]
    return b, d

def solve_query2(n, mod):
    import math
    p = mod
    a = compute_seq_lengths(n)
    k = int(math.log2(n))
    b, d = compute_b_d(n, k)
    y = product_mod(range(2, n + 1), p)
    s = k if n < 3 * (1 << (k - 1)) else 0
    total = 0
    for j in range(s, k + 1):
        e = a[:j] + [d[j]] + b[j:]
        x = y * product_mod(e, p) % p
        f = product_mod([sum(e[:i + 1]) for i in range(len(e))], p)
        while f > 1:
            t = p // f + 1
            x = x * t
            f = f * t % p
        total += x % p
    return total % p

def solve_query3(N, M, mod):
    fact, invfact = precompute_factorials(M, mod)
    if N <= 2:
        return 0
    return nCr(M, N - 1, fact, invfact, mod) * (N - 2) % mod * binpow(2, N - 3, mod) % mod
