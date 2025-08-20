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