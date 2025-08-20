from codebank import *
import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:]))
    a.sort()
    fact, invfact = precompute_factorials(2 * n, MOD)
    c = nCr(2 * n, n, fact, invfact, MOD)
    ans = c * (sum(a[n:]) - sum(a[:n])) % MOD
    print(ans)

if __name__ == "__main__":
    main()