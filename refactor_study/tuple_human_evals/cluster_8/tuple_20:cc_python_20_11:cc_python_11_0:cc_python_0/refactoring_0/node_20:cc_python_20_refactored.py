from codebank import *

CONSTANT = 998244353

def A(a, b, w, fact, invfact, mod):
    return binomial(a + b, a, fact, invfact, mod) * binomial(w + b - a - 2, b - 1, fact, invfact, mod) % mod

def V(h, W, H, fact, invfact, mod):
    s = p = 0
    for i in range(W - 1):
        p = (p + A(i, H - h, W, fact, invfact, mod)) % mod
        s = (s + p * A(W - 2 - i, h, W, fact, invfact, mod)) % mod
    return s

def main():
    H, W = map(int, input().split())
    mod = CONSTANT
    fact, invfact = precompute_factorials(H + W, mod)
    part1 = sum(V(h, W, H, fact, invfact, mod) for h in range(1, H)) % mod
    part2 = sum(V(w, H, W, fact, invfact, mod) for w in range(1, W)) % mod
    Y = sum(
        A(s, h, W, fact, invfact, mod) * A(W - 2 - s, H - h, W, fact, invfact, mod)
        for s in range(W - 1) for h in range(1, H)
    ) % mod
    X = (part1 + part2) % mod
    print((X + X - Y - Y) % mod)

if __name__ == "__main__":
    main()