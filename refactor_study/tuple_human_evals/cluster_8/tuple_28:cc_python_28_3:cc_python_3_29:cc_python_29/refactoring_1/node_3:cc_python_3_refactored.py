from codebank import *

def main():
    n = int(input())
    a = list(map(int, input().split()))
    mod = 10**9+7
    if n == 1:
        print(a[0] % mod)
        return
    k = n // 2
    fact, invfact = precompute_factorials(n, mod)
    sm1 = sm2 = 0
    for i, v in enumerate(a):
        if i % 2 == 0:
            sm1 = (sm1 + comb(k-1, i//2, fact, invfact, mod) * v) % mod
        else:
            sm2 = (sm2 + comb(k-1, i//2, fact, invfact, mod) * v) % mod
    oper = 1 if k % 2 else -1
    print((sm1 + oper * sm2) % mod)

if __name__ == "__main__":
    main()