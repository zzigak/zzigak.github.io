from codebank import *

MOD = 10**9 + 7

def main():
    n, k = map(int, input().split())
    fact, invfact = precompute_factorials(n, MOD)
    max_pairs = n // 2
    B = [0] * (max_pairs + 1)
    for i in range(max_pairs + 1):
        if n - 2 * i < 0:
            break
        # B[i] = C(n - i, i)
        B[i] = fact[n - i] * invfact[i] % MOD * invfact[n - 2 * i] % MOD
    # convolution B * B up to degree n
    A = conv(B, B, n + 1, MOD)
    # multiply by fact[n - i]
    for i in range(n + 1):
        A[i] = A[i] * fact[n - i] % MOD
    # inclusion-exclusion to pick exactly k good positions
    C = [0] * (n + 1)
    for i in range(n + 1):
        fi = fact[i]
        for j in range(i + 1):
            sign = 1 if (i - j) % 2 == 0 else -1
            C[j] = (C[j] + A[i] * fi % MOD * invfact[j] % MOD * invfact[i - j] % MOD * sign) % MOD
    print(C[k] % MOD)

if __name__ == "__main__":
    main()