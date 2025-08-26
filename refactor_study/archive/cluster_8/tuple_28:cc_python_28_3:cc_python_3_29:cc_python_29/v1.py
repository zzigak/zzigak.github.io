# ########## LIBRARY HELPERS ##########

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

def sum_matchings(n, m, fact, invfact, mod):
    lim = min(n, m)
    s = 0
    for i in range(lim + 1):
        s = (s + binomial(n, i, fact, invfact, mod) * binomial(m, i, fact, invfact, mod) * fact[i]) % mod
    return s

def alternating_reduction(a, mod):
    n = len(a)
    res = []
    sign = 1
    for i in range(n - 1):
        res.append((a[i] + sign * a[i + 1]) % mod)
        sign = -sign
    return res

def combine_sum(a, fact, invfact, mod):
    n = len(a)
    k = n // 2 - 1
    sm1 = sm2 = 0
    for i, v in enumerate(a):
        if i & 1 == 0:
            sm1 = (sm1 + binomial(k, i // 2, fact, invfact, mod) * v) % mod
        else:
            sm2 = (sm2 + binomial(k, i // 2, fact, invfact, mod) * v) % mod
    return sm1, sm2

def final_sign(n):
    return 1 if (n // 2) % 2 == 1 else -1

def compute_B(n, fact, invfact, mod):
    return [fact[n - i] * invfact[i] % mod * invfact[n - 2*i] % mod for i in range(n // 2 + 1)]

def convolution(B, C, mod, size):
    A = [0] * size
    for i, bi in enumerate(B):
        for j, cj in enumerate(C):
            if i + j < size:
                A[i + j] = (A[i + j] + bi * cj) % mod
    return A

def compute_C(A, fact, invfact, mod):
    n = len(A) - 1
    C = [0] * (n + 1)
    for i, Ai in enumerate(A):
        if Ai == 0:
            continue
        for j in range(i + 1):
            sign = 1 if ((i - j) & 1) == 0 else -1
            C[j] = (C[j] + Ai * fact[i] % mod * invfact[j] % mod * invfact[i - j] % mod * sign) % mod
    return C


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_28:cc_python_28 ##########

from codebank import *

MOD = 998244353

def main():
    a, b, c = map(int, input().split())
    n = max(a, b, c)
    fact, invfact = precompute_factorials(n, MOD)
    x = sum_matchings(a, b, fact, invfact, MOD)
    y = sum_matchings(a, c, fact, invfact, MOD)
    z = sum_matchings(b, c, fact, invfact, MOD)
    print(x * y % MOD * z % MOD)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_29:cc_python_29 ##########

from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    mod = 10**9 + 7
    n, k = map(int, input().split())
    fact, invfact = precompute_factorials(n, mod)
    B = compute_B(n, fact, invfact, mod)
    convBB = convolution(B, B, mod, n + 1)
    A = [(convBB[i] * fact[n - i]) % mod if i < len(convBB) else 0 for i in range(n + 1)]
    C = compute_C(A, fact, invfact, mod)
    print(C[k] % mod)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_3:cc_python_3 ##########

from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    mod = 10**9 + 7
    n = int(input().strip())
    a = list(map(int, input().split()))
    if n == 1:
        print(a[0] % mod)
        return
    if n & 1:
        a = alternating_reduction(a, mod)
        n -= 1
    fact, invfact = precompute_factorials(n, mod)
    sm1, sm2 = combine_sum(a, fact, invfact, mod)
    sign = final_sign(n)
    print((sm1 + sign * sm2) % mod)

if __name__ == "__main__":
    main()
