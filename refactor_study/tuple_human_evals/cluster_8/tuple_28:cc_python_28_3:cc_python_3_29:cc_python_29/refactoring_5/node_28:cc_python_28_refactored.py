from codebank import *

def main():
    a, b, c = map(int, input().split())
    mod = 998244353
    mx = max(a, b, c)
    fact, invfact = precompute_factorials(mx, mod)
    ans = sp(a, b, fact, invfact, mod)
    ans = ans * sp(a, c, fact, invfact, mod) % mod
    ans = ans * sp(b, c, fact, invfact, mod) % mod
    print(ans)

if __name__ == "__main__":
    main()