from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    N, M = map(int, data)
    MOD = 998244353
    if N <= 2:
        print(0)
        return
    fact, invfact = precompute_factorials(M, MOD)
    res = binomial(M, N-1, fact, invfact, MOD) * (N-2) % MOD * binpow(2, N-3, MOD) % MOD
    print(res)

if __name__ == "__main__":
    main()