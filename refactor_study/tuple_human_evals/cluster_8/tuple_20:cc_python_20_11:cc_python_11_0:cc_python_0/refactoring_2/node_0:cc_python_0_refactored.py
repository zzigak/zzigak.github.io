from codebank import add_mod, mul_mod, precompute_factorials, binomial
import sys

def main():
    input = sys.stdin.readline
    n, w, b = map(int, input().split())
    MOD = 1000000009
    fact, invfact = precompute_factorials(max(w, b), MOD)
    ans = 0
    for black in range(max(1, n - w), min(n - 2, b) + 1):
        term = mul_mod(
            n - 1 - black,
            mul_mod(
                binomial(w - 1, n - black - 1, fact, invfact, MOD),
                binomial(b - 1, black - 1, fact, invfact, MOD),
                MOD
            ),
            MOD
        )
        ans = add_mod(ans, term, MOD)
    ans = mul_mod(ans, fact[w], MOD)
    ans = mul_mod(ans, fact[b], MOD)
    print(ans)

if __name__ == "__main__":
    main()