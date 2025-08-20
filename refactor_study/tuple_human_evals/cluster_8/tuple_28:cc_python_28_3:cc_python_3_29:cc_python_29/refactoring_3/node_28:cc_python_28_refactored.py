from codebank import *

MOD = 998244353

def main():
    a, b, c = map(int, input().split())
    n = max(a, b, c)
    fact, invfact = precompute_factorials(n, MOD)
    x = sum_matchings(a, b, fact, invfact, MOD)
    y = sum_matchings(a, c, fact, invfact, MOD)
    z = sum_matchings(b, c, fact, invfact, MOD)
    print(x * y % MOD * z % MOD)

if __name__ == "__main__":
    main()