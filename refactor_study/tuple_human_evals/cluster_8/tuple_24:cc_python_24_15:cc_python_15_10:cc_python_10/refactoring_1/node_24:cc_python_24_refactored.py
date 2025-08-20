from codebank import *

CONSTANT = 998244353

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:]))
    mod = CONSTANT
    fact, invfact = precompute_factorials(2 * n, mod)
    a.sort()
    s1 = sum(a[:n])
    s2 = sum(a[n:])
    res = binomial(2 * n, n, fact, invfact, mod) * (s2 - s1) % mod
    print(res)

if __name__ == "__main__":
    main()