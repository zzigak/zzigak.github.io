from codebank import precompute_factorials

MOD = 998244353

def cross_ways(n, m, fact, invfact, mod):
    s = 0
    for i in range(min(n, m)+1):
        # P(n,i)=fact[n]*invfact[n-i], likewise for m, then *invfact[i]
        s = (s + fact[n]*fact[m] % mod * invfact[n-i] % mod * invfact[m-i] % mod * invfact[i]) % mod
    return s

def main():
    a, b, c = map(int, input().split())
    mx = max(a, b, c)
    fact, invfact = precompute_factorials(mx, MOD)
    ans = cross_ways(a, b, fact, invfact, MOD)
    ans = ans * cross_ways(a, c, fact, invfact, MOD) % MOD
    ans = ans * cross_ways(b, c, fact, invfact, MOD) % MOD
    print(ans)

if __name__ == "__main__":
    main()