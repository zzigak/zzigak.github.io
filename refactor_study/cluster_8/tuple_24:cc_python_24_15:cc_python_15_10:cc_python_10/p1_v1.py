# ########## PROGRAM: node_10:cc_python_10 ##########

from codebank import precompute_factorials, nCr, binpow

def main():
    import sys
    input = sys.stdin.readline
    MOD = 998244353
    n, m = map(int, input().split())
    if n <= 2:
        print(0)
        return
    fact, invfact = precompute_factorials(m, MOD)
    ans = (n - 2) * nCr(m, n - 1, fact, invfact, MOD) % MOD
    ans = ans * binpow(2, n - 3, MOD) % MOD
    print(ans)

if __name__ == "__main__":
    main()