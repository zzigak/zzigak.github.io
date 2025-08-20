from codebank import *
MOD = 10**9 + 9

def main():
    n, w, b = map(int, input().split())
    # combinations C(w-1, k) and C(b-1, k)
    factw, invw = precompute_factorials(w - 1, MOD)
    factb, invb = precompute_factorials(b - 1, MOD)
    combw = lambda k: binomial(w - 1, k, factw, invw, MOD)
    combb = lambda k: binomial(b - 1, k, factb, invb, MOD)
    ans = 0
    for black in range(max(1, n - w), min(n - 2, b) + 1):
        ans = (ans + (n - 1 - black) * combw(n - black - 1) * combb(black - 1)) % MOD
    # multiply by w! and b!
    fact_all, _ = precompute_factorials(max(w, b), MOD)
    ans = ans * fact_all[w] % MOD * fact_all[b] % MOD
    print(ans)

if __name__ == "__main__":
    main()