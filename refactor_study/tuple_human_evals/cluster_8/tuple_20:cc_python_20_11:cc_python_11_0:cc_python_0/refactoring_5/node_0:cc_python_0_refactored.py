from codebank import precompute_factorials, binomial

def main():
    n, w, b = map(int, input().split())
    mod = 10**9 + 9
    # precompute up to max(w,b)
    fact, invfact = precompute_factorials(max(w, b), mod)
    ans = 0
    lo = max(1, n - w)
    hi = min(n - 2, b)
    for black in range(lo, hi + 1):
        ways_w = binomial(w - 1, n - black - 1, fact, invfact, mod)
        ways_b = binomial(b - 1, black - 1, fact, invfact, mod)
        ans = (ans + (n - 1 - black) * ways_w % mod * ways_b) % mod
    ans = ans * fact[w] % mod * fact[b] % mod
    print(ans)

if __name__ == "__main__":
    main()