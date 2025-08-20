from codebank import *

def main():
    a, b = map(int, input().split())
    if a == b:
        print(0)
        return
    fa = factorize(a)
    fb = factorize(b)
    # compute absolute differences of exponents for 2,3,5
    diffs = [abs(fa.get(p, 0) - fb.get(p, 0)) for p in (2, 3, 5)]
    # compute the residual cofactor after removing all 2,3,5
    ra = a // (2**fa.get(2,0) * 3**fa.get(3,0) * 5**fa.get(5,0))
    rb = b // (2**fb.get(2,0) * 3**fb.get(3,0) * 5**fb.get(5,0))
    if ra != rb:
        print(-1)
    else:
        print(sum(diffs))

if __name__ == "__main__":
    main()