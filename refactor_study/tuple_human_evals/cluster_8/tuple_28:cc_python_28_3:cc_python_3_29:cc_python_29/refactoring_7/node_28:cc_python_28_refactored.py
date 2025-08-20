from codebank import *

def main():
    a, b, c = map(int, input().split())
    MOD = 998244353
    mx = max(a, b, c)
    fact, invfact = precompute_factorials(mx, MOD)
    ans = matching_count(a, b, fact, invfact, MOD)
    ans = ans * matching_count(a, c, fact, invfact, MOD) % MOD
    ans = ans * matching_count(b, c, fact, invfact, MOD) % MOD
    print(ans)

if __name__ == "__main__":
    main()