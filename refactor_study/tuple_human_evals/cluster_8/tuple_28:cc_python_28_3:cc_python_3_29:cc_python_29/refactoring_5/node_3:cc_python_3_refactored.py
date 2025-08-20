from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:]))
    mod = 10**9 + 7
    if n == 1:
        print(a[0] % mod)
        return
    # reduce to even length once if odd
    if n & 1:
        b = [(a[i] + ((-1)**i) * a[i+1]) % mod for i in range(n-1)]
        a = b
        n -= 1
    fact, invfact = precompute_factorials(n, mod)
    m2 = n // 2
    sign = 1 if m2 & 1 else -1
    sm1 = 0
    sm2 = 0
    for i in range(n):
        coef = comb(m2-1, i//2, fact, invfact, mod)
        if i & 1:
            sm2 = (sm2 + coef * a[i]) % mod
        else:
            sm1 = (sm1 + coef * a[i]) % mod
    print((sm1 + sign * sm2) % mod)

if __name__ == "__main__":
    main()