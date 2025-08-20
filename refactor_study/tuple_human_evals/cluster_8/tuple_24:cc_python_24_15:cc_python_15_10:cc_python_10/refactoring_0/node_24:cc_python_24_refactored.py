from codebank import *

def main():
    mod = 998244353
    n = int(input())
    a = list(map(int, input().split()))
    fact, invfact = precompute_factorials(2*n, mod)
    c = binomial(2*n, n, fact, invfact, mod)
    sd = sum_diff_weighted(a, n, mod)
    print(c * sd % mod)

if __name__ == "__main__":
    main()