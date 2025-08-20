from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it))
    a = [int(next(it)) for _ in range(n)]
    MOD = 1000000007
    if n == 1:
        print(a[0] % MOD)
        return
    fact, invfact = precompute_factorials(n, MOD)
    oper = 1
    # reduce rows until oper==1 and n even
    while not (oper == 1 and n % 2 == 0):
        for i in range(n - 1):
            a[i] = (a[i] + oper * a[i + 1]) % MOD
        n -= 1
        oper = -oper
    if (n // 2) % 2 == 0:
        oper = -oper
    half = n // 2 - 1
    sm1 = sm2 = 0
    for i in range(n):
        coef = comb(half, i // 2, fact, invfact, MOD)
        if i % 2 == 0:
            sm1 = (sm1 + coef * a[i]) % MOD
        else:
            sm2 = (sm2 + coef * a[i]) % MOD
    ans = (sm1 + oper * sm2) % MOD
    print(ans)

if __name__ == "__main__":
    main()