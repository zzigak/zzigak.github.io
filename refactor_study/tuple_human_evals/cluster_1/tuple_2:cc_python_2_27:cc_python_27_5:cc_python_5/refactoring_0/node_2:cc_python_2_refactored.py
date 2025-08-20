from codebank import *

PRIMES = (2, 3, 5)

def main():
    import sys
    a, b = map(int, sys.stdin.read().split())
    if a == b:
        print(0)
        return
    fa = factorize(a)
    fb = factorize(b)
    # count operations on 2,3,5
    ops = sum(abs(fa.get(p, 0) - fb.get(p, 0)) for p in PRIMES)
    # check residuals
    if residual_after_factors(a, PRIMES) != residual_after_factors(b, PRIMES):
        print(-1)
    else:
        print(ops)

if __name__ == "__main__":
    main()