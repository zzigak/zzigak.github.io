from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    n, k = map(int, data)
    mod = 10**9 + 7
    fact, invfact = precompute_factorials(n, mod)
    # B[i] = (n-i)! / (i! * (n-2i)!)
    B = [0] * (n//2 + 1)
    for i in range(len(B)):
        B[i] = fact[n-i] * invfact[i] % mod * invfact[n-2*i] % mod
    A = convolution(B, B, n+1, mod)
    for i in range(n+1):
        A[i] = A[i] * fact[n-i] % mod
    C = [0] * (n+1)
    for i in range(n+1):
        Ai = A[i]
        for j in range(i+1):
            sign = 1 if ((i-j) & 1) == 0 else -1
            C[j] = (C[j] + Ai * comb(i, j, fact, invfact, mod) * sign) % mod
    print(C[k] % mod)

if __name__ == "__main__":
    main()