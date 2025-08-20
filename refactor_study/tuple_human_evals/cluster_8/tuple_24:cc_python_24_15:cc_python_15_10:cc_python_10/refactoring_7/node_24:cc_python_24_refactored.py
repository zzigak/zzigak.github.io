from codebank import *

CONSTANT = 998244353

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:]))
    a.sort()
    fact, invfact = precompute_factorials(2*n, CONSTANT)
    c = binomial(2*n, n, fact, invfact, CONSTANT)
    diff = sum(a[n:]) - sum(a[:n])
    print(c * (diff % CONSTANT) % CONSTANT)

if __name__ == "__main__":
    main()