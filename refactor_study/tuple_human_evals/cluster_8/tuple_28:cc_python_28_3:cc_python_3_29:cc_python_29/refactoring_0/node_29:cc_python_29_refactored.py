from codebank import *
import sys

CONSTANT = 10**9 + 7

def main():
    n, k = map(int, sys.stdin.readline().split())
    fact, invfact = precompute_factorials(n, CONSTANT)
    B = [0] * (n + 1)
    for i in range(n + 1):
        if i * 2 <= n:
            B[i] = fact[n - i] * invfact[i] % CONSTANT * invfact[n - 2 * i] % CONSTANT
    A = convolve(B, B, CONSTANT)[:n+1]
    for i in range(n + 1):
        A[i] = A[i] * fact[n - i] % CONSTANT
    C = [0] * (n + 1)
    for i in range(n + 1):
        for j in range(i + 1):
            sign = 1 if ((i - j) % 2 == 0) else -1
            C[j] = (C[j] + A[i] * comb(i, j, fact, invfact, CONSTANT) * sign) % CONSTANT
    print(C[k] % CONSTANT)

if __name__ == "__main__":
    main()