from codebank import precompute_factorials, binomial

def count_A(a, b, w, mod, fact, invfact):
    return binomial(a + b, a, fact, invfact, mod) * binomial(w + b - a - 2, b - 1, fact, invfact, mod) % mod

def count_V(h, W, H, mod, fact, invfact):
    s = 0
    p = 0
    for i in range(W - 1):
        p = (p + count_A(i, H - h, W, mod, fact, invfact)) % mod
        s = (s + p * count_A(W - 2 - i, h, W, mod, fact, invfact)) % mod
    return s

def main():
    n, m = map(int, input().split())
    mod = 998244353
    fact, invfact = precompute_factorials(n + m, mod)
    Y = 0
    for s in range(m - 1):
        for h in range(1, n):
            Y = (Y + count_A(s, h, m, mod, fact, invfact) * count_A(m - 2 - s, n - h, m, mod, fact, invfact)) % mod
    X = 0
    for h in range(1, n):
        X = (X + count_V(h, m, n, mod, fact, invfact)) % mod
    for w in range(1, m):
        X = (X + count_V(w, n, m, mod, fact, invfact)) % mod
    print(2 * (X - Y) % mod)

if __name__ == "__main__":
    main()