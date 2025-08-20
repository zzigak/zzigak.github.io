from codebank import *

CONSTANT = 998244353

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:]))
    mod = CONSTANT
    a.sort()
    fact, invfact = precompute_factorials(2 * n, mod)
    c = binomial(2 * n, n, fact, invfact, mod)
    diff = (sum(a[n:]) - sum(a[:n])) % mod
    print(c * diff % mod)

if __name__ == "__main__":
    main()