from codebank import *

MOD = 998244353

def main():
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    total = (sum(a[n:]) - sum(a[:n])) % MOD
    fact, invfact = precompute_factorials(2 * n, MOD)
    ways = binomial(2 * n, n, fact, invfact, MOD)
    print(ways * total % MOD)

if __name__ == "__main__":
    main()