from codebank import binpow, precompute_factorials, comb

def main():
    import sys
    input = sys.stdin.readline
    mod = 998244353
    N, M = map(int, input().split())
    if N <= 2:
        print(0)
        return
    fact, invfact = precompute_factorials(M, mod)
    c = comb(M, N-1, fact, invfact, mod)
    res = c * (N-2) % mod * binpow(2, N-3, mod) % mod
    print(res)

if __name__ == "__main__":
    main()