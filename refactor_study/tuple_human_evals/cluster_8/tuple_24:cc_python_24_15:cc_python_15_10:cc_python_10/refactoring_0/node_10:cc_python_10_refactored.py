from codebank import *

MOD = 998244353

def main():
    n, m = map(int, input().split())
    if n <= 2:
        res = 0
    else:
        fact, invfact = precompute_factorials(m, MOD)
        c = binomial(m, n - 1, fact, invfact, MOD)
        res = c * (n - 2) % MOD * binpow(2, n - 3, MOD) % MOD
    print(res)

if __name__ == "__main__":
    main()