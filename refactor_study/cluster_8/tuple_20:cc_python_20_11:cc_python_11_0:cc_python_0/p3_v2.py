# ########## PROGRAM: node_20:cc_python_20 ##########

from codebank import *

MOD = 998244353

def main():
    H, W = map(int, input().split())
    fact, invfact = precompute_factorials(H + W, MOD)
    Y = 0
    for s in range(W - 1):
        for h in range(1, H):
            Y = (Y + A(s, h, W, fact, invfact, MOD) *
                     A(W - 2 - s, H - h, W, fact, invfact, MOD)) % MOD
    X = 0
    for h in range(1, H):
        X = (X + V(h, W, H, fact, invfact, MOD)) % MOD
    for w in range(1, W):
        X = (X + V(w, H, W, fact, invfact, MOD)) % MOD
    print((X * 2 - Y * 2) % MOD)

if __name__ == "__main__":
    main()