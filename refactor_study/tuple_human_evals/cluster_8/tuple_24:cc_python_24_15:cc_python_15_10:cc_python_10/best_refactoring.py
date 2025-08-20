# ########## LIBRARY HELPERS ##########

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
    while y > 0:
        if y & 1:
            result = result * x % mod
        x = x * x % mod
        y >>= 1
    return result

def nCr(n, r, fact, invfact, mod):
    if r < 0 or r > n:
        return 0
    return fact[n] * invfact[r] % mod * invfact[n - r] % mod

def prod(nums, mod):
    result = 1
    for x in nums:
        result = result * x % mod
    return result


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_10:cc_python_10 ##########

from codebank import precompute_factorials, nCr, binpow

def main():
    import sys
    input = sys.stdin.readline
    MOD = 998244353
    n, m = map(int, input().split())
    if n <= 2:
        print(0)
        return
    fact, invfact = precompute_factorials(m, MOD)
    ans = (n - 2) * nCr(m, n - 1, fact, invfact, MOD) % MOD
    ans = ans * binpow(2, n - 3, MOD) % MOD
    print(ans)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_15:cc_python_15 ##########

from codebank import prod
import math

def main():
    mod = 10**9 + 7
    n = int(input())
    x = n
    a = []
    while x > 0:
        a.append(x - x // 2)
        x //= 2
    k = int(math.log2(n))
    b = [n // (3 * (1 << i)) - n // (6 * (1 << i)) for i in range(k + 1)]
    d = [n // (1 << i) - n // (3 * (1 << i)) for i in range(k + 1)]
    y = prod(range(2, n + 1), mod)
    t = 0
    s = k if n < 3 * (1 << (k - 1)) else 0
    for j in range(s, k + 1):
        e = [a[i] for i in range(j)] + [d[j]] + [b[i] for i in range(j, k)]
        x_val = y * prod(e, mod) % mod
        f_val = prod([sum(e[:i+1]) for i in range(k + 1)], mod)
        while f_val > 1:
            x_val *= mod // f_val + 1
            f_val = f_val * (mod // f_val + 1) % mod
        t = (t + x_val) % mod
    print(t)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_24:cc_python_24 ##########

from codebank import precompute_factorials, nCr

def main():
    import sys
    input = sys.stdin.readline
    mod = 998244353
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    fact, invfact = precompute_factorials(2 * n, mod)
    ans = nCr(2 * n, n, fact, invfact, mod) * (sum(a[n:]) - sum(a[:n])) % mod
    print(ans)

if __name__ == "__main__":
    main()
