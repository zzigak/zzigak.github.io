from codebank import *

MOD = 998244353

def main():
    a, b, c = map(int, input().split())
    N = max(a, b, c)
    fact, invfact = precompute_factorials(N, MOD)
    ans = sp(a, b, fact, invfact, MOD) * sp(a, c, fact, invfact, MOD) % MOD * sp(b, c, fact, invfact, MOD) % MOD
    print(ans)

if __name__ == "__main__":
    main()