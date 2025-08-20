from codebank import *

CONSTANT = 998244353

def main():
    import sys
    N, M = map(int, sys.stdin.read().split())
    if N <= 2:
        print(0)
        return
    fact, invfact = precompute_factorials(M, CONSTANT)
    ans = binomial(M, N - 1, fact, invfact, CONSTANT)
    ans = ans * (N - 2) % CONSTANT * pow(2, N - 3, CONSTANT) % CONSTANT
    print(ans)

if __name__ == "__main__":
    main()