from codebank import *

def main():
    a, b, c = map(int, input().split())
    MOD = 998244353
    m = max(a, b, c)
    fact, invfact = precompute_factorials(m, MOD)
    ans = series_pair(a, b, fact, invfact, MOD)
    ans = ans * series_pair(a, c, fact, invfact, MOD) % MOD
    ans = ans * series_pair(b, c, fact, invfact, MOD) % MOD
    print(ans)

if __name__ == "__main__":
    main()