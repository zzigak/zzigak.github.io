from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    mod = 1000000007
    n, k = map(int, input().split())
    fact, invfact = precompute_factorials(n, mod)
    half = n // 2
    B = [comb(n - i, i, fact, invfact, mod) for i in range(half + 1)]
    A = [0] * (n + 1)
    for i in range(len(B)):
        for j in range(len(B)):
            if i + j <= n:
                A[i + j] = (A[i + j] + B[i] * B[j]) % mod
    for i in range(n + 1):
        A[i] = A[i] * fact[n - i] % mod
    res = 0
    for i in range(k, n + 1):
        term = A[i] * comb(i, k, fact, invfact, mod) % mod
        if (i - k) & 1:
            res = (res - term) % mod
        else:
            res = (res + term) % mod
    print(res)

if __name__ == "__main__":
    main()