from codebank import precompute_factorials, binomial

def main():
    n, k = map(int, input().split())
    mod = 10**9+7
    fact, invfact = precompute_factorials(n, mod)
    # B[i] = C(n-i, i)
    m = n//2
    B = [0]*(m+1)
    for i in range(m+1):
        B[i] = binomial(n-i, i, fact, invfact, mod)
    # convolution A = B*B
    A = [0]*(n+1)
    for i in range(m+1):
        for j in range(m+1):
            A[i+j] = (A[i+j] + B[i]*B[j]) % mod
    # multiply by (n-i)!
    for i in range(n+1):
        A[i] = A[i] * fact[n-i] % mod
    # C[j] = sum_{i>=j} A[i] * C(i,j) * sign
    C = [0]*(n+1)
    for i in range(n+1):
        for j in range(i+1):
            sign = 1 - 2*((i-j)&1)
            C[j] = (C[j] + A[i] * binomial(i, j, fact, invfact, mod) * sign) % mod
    print(C[k] % mod)

if __name__ == "__main__":
    main()