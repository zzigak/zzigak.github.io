from codebank import *

def main():
    a, b, c = map(int, input().split())
    mod = 998244353
    nmax = max(a, b, c)
    fact, invfact = precompute_factorials(nmax, mod)
    res = sp(a, b, fact, invfact, mod)
    res = res * sp(a, c, fact, invfact, mod) % mod
    res = res * sp(b, c, fact, invfact, mod) % mod
    print(res)

if __name__ == "__main__":
    main()