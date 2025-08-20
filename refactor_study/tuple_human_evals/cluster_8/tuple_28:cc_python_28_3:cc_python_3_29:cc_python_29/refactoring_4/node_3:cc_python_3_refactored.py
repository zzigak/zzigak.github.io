from codebank import *

MOD = 10**9 + 7

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0]); a = list(map(int, data[1:]))
    if n == 1:
        print(a[0] % MOD)
        return
    if n % 2 == 1:
        a = compress(a, MOD)
        n -= 1
    sign = sign_coeff(n)
    fact, invfact = precompute_factorials(n, MOD)
    m = n // 2 - 1
    sm1 = sm2 = 0
    for i, v in enumerate(a):
        idx = i // 2
        if idx > m:
            break
        coef = fact[m] * invfact[idx] % MOD * invfact[m - idx] % MOD
        if i % 2 == 0:
            sm1 = (sm1 + coef * v) % MOD
        else:
            sm2 = (sm2 + coef * v) % MOD
    print((sm1 + sign * sm2) % MOD)

if __name__ == "__main__":
    main()