from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    N = int(data[0])
    M = int(data[1])
    mod = 998244353
    if N <= 2:
        print(0)
        return
    fact, invfact = precompute_factorials(M, mod)
    c = binomial(M, N - 1, fact, invfact, mod)
    res = c * (N - 2) % mod * binpow(2, N - 3, mod) % mod
    print(res)

if __name__ == "__main__":
    main()