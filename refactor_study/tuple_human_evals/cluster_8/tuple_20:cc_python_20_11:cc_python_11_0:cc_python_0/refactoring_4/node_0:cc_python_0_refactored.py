from codebank import *

def main():
    MOD = 10**9 + 9
    n, w, b = map(int, input().split())
    min_black = max(1, n - w)
    max_black = min(n - 2, b)
    if min_black > max_black:
        print(0)
        return
    fact, invfact = precompute_factorials(max(w, b), MOD)
    ans = 0
    for black in range(min_black, max_black + 1):
        white_days = n - black
        ways_days = n - 1 - black
        ways_white = binomial(w - 1, white_days - 1, fact, invfact, MOD)
        ways_black = binomial(b - 1, black - 1, fact, invfact, MOD)
        ans = (ans + ways_days * ways_white % MOD * ways_black) % MOD
    ans = ans * fact[w] % MOD * fact[b] % MOD
    print(ans)

if __name__ == "__main__":
    main()