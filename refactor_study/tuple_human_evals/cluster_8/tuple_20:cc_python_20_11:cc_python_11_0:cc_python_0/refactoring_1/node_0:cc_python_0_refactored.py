from codebank import *

MOD = 10**9 + 9

def main():
    n, w, b = map(int, input().split())
    fact, invfact = precompute_factorials(max(w, b), MOD)
    ans = 0
    for black in range(max(1, n - w), min(n - 2, b) + 1):
        white_days = n - black
        ans = (ans +
               (white_days - 1) *
               binomial(w - 1, white_days - 1, fact, invfact, MOD) *
               binomial(b - 1, black - 1, fact, invfact, MOD)) % MOD
    ans = ans * fact[w] % MOD * fact[b] % MOD
    print(ans)

if __name__ == "__main__":
    main()