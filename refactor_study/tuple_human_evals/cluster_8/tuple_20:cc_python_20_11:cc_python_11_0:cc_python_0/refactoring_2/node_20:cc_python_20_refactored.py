from codebank import add_mod, mul_mod, sum_mod, precompute_factorials, binomial
import sys

def A(a, b, w, fact, invfact, M):
    return mul_mod(
        binomial(a + b, a, fact, invfact, M),
        binomial(w + b - a - 2, b - 1, fact, invfact, M),
        M
    )

def V(h, W, H, fact, invfact, M):
    s = 0
    p = 0
    for i in range(W - 1):
        p = add_mod(p, A(i, H - h, W, fact, invfact, M), M)
        s = add_mod(s, mul_mod(p, A(W - 2 - i, h, W, fact, invfact, M), M), M)
    return s

def main():
    input = sys.stdin.readline
    M = 998244353
    H, W = map(int, input().split())
    N = H + W
    fact, invfact = precompute_factorials(N, M)
    Y = sum_mod(
        (
            mul_mod(
                A(s, h, W, fact, invfact, M),
                A(W - 2 - s, H - h, W, fact, invfact, M),
                M
            )
            for s in range(W - 1)
            for h in range(1, H)
        ),
        M
    )
    X1 = sum_mod((V(h, W, H, fact, invfact, M) for h in range(1, H)), M)
    X2 = sum_mod((V(w, H, W, fact, invfact, M) for w in range(1, W)), M)
    X = add_mod(X1, X2, M)
    ans = (mul_mod(X, 2, M) - mul_mod(Y, 2, M)) % M
    print(ans)

if __name__ == "__main__":
    main()