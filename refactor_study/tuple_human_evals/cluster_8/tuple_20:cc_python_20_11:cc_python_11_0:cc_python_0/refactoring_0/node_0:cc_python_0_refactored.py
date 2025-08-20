from codebank import *

CONSTANT = 10**9 + 9

def count_config(n, w, b, fact, invfact, mod):
    res = 0
    lo = max(1, n - w)
    hi = min(n - 2, b)
    for k in range(lo, hi + 1):
        term = (n - 1 - k) * binomial(w - 1, n - k - 1, fact, invfact, mod) % mod
        term = term * binomial(b - 1, k - 1, fact, invfact, mod) % mod
        res = (res + term) % mod
    return res * fact[w] % mod * fact[b] % mod

def main():
    n, w, b = map(int, input().split())
    mod = CONSTANT
    fact, invfact = precompute_factorials(max(w, b), mod)
    print(count_config(n, w, b, fact, invfact, mod))

if __name__ == "__main__":
    main()