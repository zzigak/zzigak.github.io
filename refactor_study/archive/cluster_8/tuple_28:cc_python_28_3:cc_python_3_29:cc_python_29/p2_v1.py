# ########## PROGRAM: node_29:cc_python_29 ##########

from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    mod = 10**9 + 7
    n, k = map(int, input().split())
    fact, invfact = precompute_factorials(n, mod)
    B = compute_B(n, fact, invfact, mod)
    convBB = convolution(B, B, mod, n + 1)
    A = [(convBB[i] * fact[n - i]) % mod if i < len(convBB) else 0 for i in range(n + 1)]
    C = compute_C(A, fact, invfact, mod)
    print(C[k] % mod)

if __name__ == "__main__":
    main()