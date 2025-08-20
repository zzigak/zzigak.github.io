from codebank import *

MOD = 998244353

def main():
    N, M = map(int, input().split())
    if N <= 2:
        print(0)
        return
    fact, invfact = precompute_factorials(M, MOD)
    c = binomial(M, N - 1, fact, invfact, MOD)
    res = c * (N - 2) % MOD * binpow(2, N - 3, MOD) % MOD
    print(res)

if __name__ == "__main__":
    main()