from codebank import *

def main():
    MOD = 998244353
    H, W = map(int, input().split())
    fact, invfact = precompute_factorials(H + W, MOD)
    Y = 0
    for s in range(W - 1):
        for h in range(1, H):
            Y = mod_add(
                Y,
                mod_mul(
                    compute_A(s, h, W, fact, invfact, MOD),
                    compute_A(W - 2 - s, H - h, W, fact, invfact, MOD),
                    MOD
                ),
                MOD
            )
    X = (
        sum(compute_V(h, W, H, fact, invfact, MOD) for h in range(1, H)) +
        sum(compute_V(w, H, W, fact, invfact, MOD) for w in range(1, W))
    ) % MOD
    print((2 * X - 2 * Y) % MOD)

if __name__ == "__main__":
    main()