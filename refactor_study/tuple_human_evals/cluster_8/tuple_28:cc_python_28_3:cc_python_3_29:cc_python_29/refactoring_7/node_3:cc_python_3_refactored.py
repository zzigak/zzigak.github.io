from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:]))
    MOD = 10**9 + 7
    if n == 1:
        print(a[0] % MOD)
        return
    fact, invfact = precompute_factorials(n, MOD)
    oper = 1
    # reduce length until n is even
    while n & 1:
        for i in range(n - 1):
            a[i] = (a[i] + oper * a[i + 1]) % MOD
            oper = -oper
        n -= 1
    oper *= 1 if ((n // 2) & 1) else -1
    half = n // 2 - 1
    sm1 = sm2 = 0
    for i in range(n):
        c = binomial(half, i // 2, fact, invfact, MOD)
        if i & 1:
            sm2 = (sm2 + c * a[i]) % MOD
        else:
            sm1 = (sm1 + c * a[i]) % MOD
    print((sm1 + oper * sm2) % MOD)

if __name__ == "__main__":
    main()