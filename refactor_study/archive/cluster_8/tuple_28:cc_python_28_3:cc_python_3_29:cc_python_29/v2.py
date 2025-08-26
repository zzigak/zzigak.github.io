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

def matching_count(n, m, fact, invfact, mod):
    limit = min(n, m)
    res = 0
    for i in range(limit + 1):
        res = (res + binomial(n, i, fact, invfact, mod)
                   * binomial(m, i, fact, invfact, mod)
                   * fact[i]) % mod
    return res


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_28:cc_python_28 ##########

from codebank import *

def main():
    a, b, c = map(int, input().split())
    MOD = 998244353
    mx = max(a, b, c)
    fact, invfact = precompute_factorials(mx, MOD)
    ans = matching_count(a, b, fact, invfact, MOD)
    ans = ans * matching_count(a, c, fact, invfact, MOD) % MOD
    ans = ans * matching_count(b, c, fact, invfact, MOD) % MOD
    print(ans)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_29:cc_python_29 ##########

from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    n, k = map(int, data[:2])
    MOD = 10**9 + 7
    fact, invfact = precompute_factorials(n, MOD)
    maxp = n // 2
    B = [0] * (maxp + 1)
    for i in range(maxp + 1):
        B[i] = binomial(n - i, i, fact, invfact, MOD)
    A = [0] * (n + 1)
    for i in range(maxp + 1):
        for j in range(maxp + 1):
            t = i + j
            if t <= n:
                A[t] = (A[t] + B[i] * B[j]) % MOD
    for i in range(n + 1):
        A[i] = A[i] * fact[n - i] % MOD
    C = [0] * (n + 1)
    for i in range(n + 1):
        for j in range(i + 1):
            sign = 1 if ((i - j) & 1) == 0 else -1
            C[j] = (C[j] + A[i] * fact[i] % MOD
                    * invfact[j] % MOD
                    * invfact[i - j] % MOD
                    * sign) % MOD
    print(C[k] % MOD)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_3:cc_python_3 ##########

from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:]))
    MOD = 10**9 + 7
    if n == 1:
        print(a[0] % MOD)
        return
    fact, invfact = precompute_factorials(n, MOD)
    oper = 1
    # reduce length until n is even
    while n & 1:
        for i in range(n - 1):
            a[i] = (a[i] + oper * a[i + 1]) % MOD
            oper = -oper
        n -= 1
    oper *= 1 if ((n // 2) & 1) else -1
    half = n // 2 - 1
    sm1 = sm2 = 0
    for i in range(n):
        c = binomial(half, i // 2, fact, invfact, MOD)
        if i & 1:
            sm2 = (sm2 + c * a[i]) % MOD
        else:
            sm1 = (sm1 + c * a[i]) % MOD
    print((sm1 + oper * sm2) % MOD)

if __name__ == "__main__":
    main()
