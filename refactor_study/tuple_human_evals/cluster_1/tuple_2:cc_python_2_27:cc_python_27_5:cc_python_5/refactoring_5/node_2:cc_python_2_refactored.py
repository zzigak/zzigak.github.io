from codebank import *

def main():
    import sys
    a, b = map(int, sys.stdin.readline().split())
    if a == b:
        print(0)
        return
    fa = factorize(a)
    fb = factorize(b)
    primes = [2, 3, 5]
    ea = [fa.get(p, 0) for p in primes]
    eb = [fb.get(p, 0) for p in primes]
    x, y = a, b
    for p, e in zip(primes, ea):
        x //= p**e
    for p, e in zip(primes, eb):
        y //= p**e
    if x != y:
        print(-1)
    else:
        print(sum(abs(u - v) for u, v in zip(ea, eb)))

if __name__ == "__main__":
    main()