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
    result = 1
    x %= mod
    while y:
        if y & 1:
            result = result * x % mod
        x = x * x % mod
        y >>= 1
    return result

def modinv(x, mod):
    return binpow(x, mod - 2, mod)

def precompute_factorials(limit, mod):
    fact = [1] * (limit + 1)
    invfact = [1] * (limit + 1)
    for i in range(1, limit + 1):
        fact[i] = fact[i - 1] * i % mod
    invfact[limit] = modinv(fact[limit], mod)
    for i in range(limit, 0, -1):
        invfact[i - 1] = invfact[i] * i % mod
    return fact, invfact

def binomial(n, k, fact, invfact, mod):
    if k < 0 or k > n:
        return 0
    return fact[n] * invfact[k] % mod * invfact[n - k] % mod

def product(lst, mod):
    result = 1
    for v in lst:
        result = result * v % mod
    return result
