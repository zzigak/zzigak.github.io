from codebank import *
import sys

CONSTANT = 998244353

def main():
    a, b, c = map(int, sys.stdin.readline().split())
    fact, invfact = precompute_factorials(max(a, b, c), CONSTANT)
    res = sp(a, b, fact, invfact, CONSTANT)
    res = res * sp(a, c, fact, invfact, CONSTANT) % CONSTANT
    res = res * sp(b, c, fact, invfact, CONSTANT) % CONSTANT
    print(res)

if __name__ == "__main__":
    main()