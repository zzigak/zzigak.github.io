from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    mod = 10**9+7
    n, k = map(int, input().split())
    fact, invfact = precompute_factorials(n, mod)
    B = [comb(n-i, i, fact, invfact, mod) for i in range(n+1)]
    A = [0] * (n + 1)
    for i, bi in enumerate(B):
        if bi:
            for j in range(n+1-i):
                A[i+j] = (A[i+j] + bi * B[j]) % mod
    for i in range(n+1):
        A[i] = A[i] * fact[n-i] % mod
    C = [0] * (n + 1)
    for i, Ai in enumerate(A):
        if Ai:
            for j in range(i+1):
                sign = 1 if ((i-j) & 1) == 0 else -1
                C[j] = (C[j] + Ai * comb(i, j, fact, invfact, mod) * sign) % mod
    print(C[k] % mod)

if __name__ == "__main__":
    main()