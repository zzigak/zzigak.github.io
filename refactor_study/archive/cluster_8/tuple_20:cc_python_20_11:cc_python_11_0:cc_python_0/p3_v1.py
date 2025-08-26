# ########## PROGRAM: node_20:cc_python_20 ##########

from codebank import precompute_factorials, binomial

def main():
    M = 998244353
    H, W = map(int, input().split())
    fact, invfact = precompute_factorials(H + W, M)

    def A(a, b, w):
        return binomial(a + b, a, fact, invfact, M) * binomial(w + b - a - 2, b - 1, fact, invfact, M) % M

    def V(h, W, H):
        s = 0
        p = 0
        for i in range(W - 1):
            p = (p + A(i, H - h, W)) % M
            s = (s + p * A(W - 2 - i, h, W)) % M
        return s

    Y = 0
    for s in range(W - 1):
        for h in range(1, H):
            Y = (Y + A(s, h, W) * A(W - 2 - s, H - h, W)) % M

    X = 0
    for h in range(1, H):
        X = (X + V(h, W, H)) % M
    for w in range(1, W):
        X = (X + V(w, H, W)) % M

    print((2 * X - 2 * Y) % M)

if __name__ == "__main__":
    main()