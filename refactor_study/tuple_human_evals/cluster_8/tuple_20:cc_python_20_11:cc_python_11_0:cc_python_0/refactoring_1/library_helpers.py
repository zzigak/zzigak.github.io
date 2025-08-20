# ==== RETRIEVED HELPER FUNCTIONS ====
def binomial(n, k, fact, invfact, mod):
    # Success rate: 8/8

    if k < 0 or k > n:
        return 0
    return fact[n] * invfact[k] % mod * invfact[n - k] % mod

def factorials(n):
    # Success rate: 1/1

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i
    return fact

def binpow(x, y, mod):
    # Success rate: 1/1

    result = 1
    x %= mod
    while y > 0:
        if y & 1:
            result = result * x % mod
        x = x * x % mod
        y >>= 1
    return result

def factorize(x):
    # Success rate: 1/1

    d = {}
    while x % 2 == 0:
        d[2] = d.get(2, 0) + 1
        x //= 2
    i = 3
    while i * i <= x:
        while x % i == 0:
            d[i] = d.get(i, 0) + 1
            x //= i
        i += 2
    if x > 1:
        d[x] = d.get(x, 0) + 1
    return d

def geo_sum(r, t, mod):
    # Success rate: 2/2

    r %= mod
    if r == 1:
        return t % mod
    return (pow(r, t, mod) - 1) * modinv(r - 1, mod) % mod

def precompute_factorials(n, mod):
    # Success rate: 11/11

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

def A(a, b, w, fact, invfact, mod):
    return binomial(a + b, a, fact, invfact, mod) * \
           binomial(w + b - a - 2, b - 1, fact, invfact, mod) % mod

def V(h, W, H, fact, invfact, mod):
    s = 0
    p = 0
    for i in range(W - 1):
        p = (p + A(i, H - h, W, fact, invfact, mod)) % mod
        s = (s + p * A(W - 2 - i, h, W, fact, invfact, mod)) % mod
    return s
