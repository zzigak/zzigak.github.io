# ########## LIBRARY HELPERS ##########

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


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_0:cc_python_0 ##########

from codebank import *

MOD = 10**9 + 9

def main():
    n, w, b = map(int, input().split())
    fact, invfact = precompute_factorials(max(w, b), MOD)
    ans = 0
    for black in range(max(1, n - w), min(n - 2, b) + 1):
        white_days = n - black
        ans = (ans +
               (white_days - 1) *
               binomial(w - 1, white_days - 1, fact, invfact, MOD) *
               binomial(b - 1, black - 1, fact, invfact, MOD)) % MOD
    ans = ans * fact[w] % MOD * fact[b] % MOD
    print(ans)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_11:cc_python_11 ##########

from codebank import *

MOD = 998244853

def main():
    a, b = map(int, input().split())
    total = a + b
    if total == 0:
        print(0)
        return
    fact, invfact = precompute_factorials(total, MOD)
    C = lambda n, k: binomial(n, k, fact, invfact, MOD)
    min_lv = max(0, a - b)
    max_lv = a
    res = min_lv * C(total, a) % MOD
    for lv in range(min_lv + 1, max_lv + 1):
        t = 2 * lv - a + b
        idx = (total + t) // 2
        res = (res + C(total, idx)) % MOD
    print(res)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_20:cc_python_20 ##########

from codebank import *

MOD = 998244353

def main():
    H, W = map(int, input().split())
    fact, invfact = precompute_factorials(H + W, MOD)
    Y = 0
    for s in range(W - 1):
        for h in range(1, H):
            Y = (Y + A(s, h, W, fact, invfact, MOD) *
                     A(W - 2 - s, H - h, W, fact, invfact, MOD)) % MOD
    X = 0
    for h in range(1, H):
        X = (X + V(h, W, H, fact, invfact, MOD)) % MOD
    for w in range(1, W):
        X = (X + V(w, H, W, fact, invfact, MOD)) % MOD
    print((X * 2 - Y * 2) % MOD)

if __name__ == "__main__":
    main()
