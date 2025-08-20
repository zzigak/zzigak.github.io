from codebank import *
M = 998244353

def main():
    H, W = map(int, input().split())
    fact, invfact = precompute_factorials(H + W + 5, M)
    Y = 0
    for s in range(W - 1):
        for h in range(1, H):
            Y = mod_add(
                Y,
                mod_mul(
                    calc_A(s, h, W, fact, invfact, M),
                    calc_A(W - 2 - s, H - h, W, fact, invfact, M),
                    M
                ),
                M
            )
    X = 0
    for h in range(1, H):
        X = mod_add(X, calc_V(h, W, H, fact, invfact, M), M)
    for w in range(1, W):
        X = mod_add(X, calc_V(w, H, W, fact, invfact, M), M)
    print((2 * X - 2 * Y) % M)

if __name__ == "__main__":
    main()