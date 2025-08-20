# ==== RETRIEVED HELPER FUNCTIONS ====
def comb(n, k, fact):
    # Success rate: 2/2

    if k < 0 or k > n:
        return 0
    return fact[n] // (fact[k] * fact[n - k])

def binomial(n, k, fact, invfact, mod):
    # Success rate: 14/14

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

def prod(nums, mod):
    # Success rate: 1/1

    result = 1
    for x in nums:
        result = result * x % mod
    return result

def geo_sum(r, t, mod):
    # Success rate: 2/2

    r %= mod
    if r == 1:
        return t % mod
    return (pow(r, t, mod) - 1) * modinv(r - 1, mod) % mod

def precompute_factorials(n, mod):
    # Success rate: 17/17

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

def sp(n, m, fact, invfact, mod):
    res = 0
    fn, fm = fact[n], fact[m]
    for i in range(min(n, m) + 1):
        res = (res + fn * invfact[n - i] % mod * fm * invfact[m - i] % mod * invfact[i]) % mod
    return res

def compress(a, mod):
    new = [0] * (len(a) - 1)
    op = 1
    for i in range(len(new)):
        new[i] = (a[i] + op * a[i + 1]) % mod
        op = -op
    return new

def sign_coeff(n):
    return 1 if ((n // 2) % 2) else -1

def conv(a, b, length, mod):
    c = [0] * length
    for i in range(length):
        s = 0
        for j in range(i + 1):
            s += a[j] * b[i - j]
        c[i] = s % mod
    return c
