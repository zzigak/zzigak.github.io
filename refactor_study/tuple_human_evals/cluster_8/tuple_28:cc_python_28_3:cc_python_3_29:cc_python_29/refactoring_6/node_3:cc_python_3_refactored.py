from codebank import precompute_factorials, binpow, binomial

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:]))
    mod = 10**9+7
    if n == 1:
        print(a[0] % mod)
        return
    oper = 1
    # reduce once if odd
    while n & 1:
        for i in range(n-1):
            a[i] = (a[i] + oper * a[i+1]) % mod
            oper = -oper
        n -= 1
    # adjust starting operation for final combine
    oper *= 1 if ((n//2) & 1) else -1
    fact, invfact = precompute_factorials(n, mod)
    sm1 = sm2 = 0
    half = n//2 - 1
    for i in range(n):
        if i & 1:
            sm2 = (sm2 + binomial(half, i//2, fact, invfact, mod) * a[i]) % mod
        else:
            sm1 = (sm1 + binomial(half, i//2, fact, invfact, mod) * a[i]) % mod
    print((sm1 + oper * sm2) % mod)

if __name__ == "__main__":
    main()