from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    mod = 998244353
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    fact, invfact = precompute_factorials(2*n, mod)
    choose = comb(2*n, n, fact, invfact, mod)
    diff = (sum(a[n:]) - sum(a[:n])) % mod
    print(choose * diff % mod)

if __name__ == "__main__":
    main()