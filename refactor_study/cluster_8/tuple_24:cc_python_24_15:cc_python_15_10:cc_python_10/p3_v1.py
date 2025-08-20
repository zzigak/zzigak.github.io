# ########## PROGRAM: node_24:cc_python_24 ##########

from codebank import precompute_factorials, nCr

def main():
    import sys
    input = sys.stdin.readline
    mod = 998244353
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    fact, invfact = precompute_factorials(2 * n, mod)
    ans = nCr(2 * n, n, fact, invfact, mod) * (sum(a[n:]) - sum(a[:n])) % mod
    print(ans)

if __name__ == "__main__":
    main()