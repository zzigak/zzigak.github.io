from codebank import *
from math import asin

def main():
    c1 = tuple(map(int, input().split()))
    c2 = tuple(map(int, input().split()))
    c3 = tuple(map(int, input().split()))
    l1 = get_locus(c1, c2)
    l2 = get_locus(c1, c3)
    pts = intersect_loci(l1, l2)
    if not pts:
        return
    best = None
    bestang = -1.0
    x1,y1,r1 = c1
    for x,y in pts:
        d = hypot(x-x1, y-y1)
        if d <= 0: 
            continue
        ang = asin(r1/d)
        if ang > bestang:
            bestang = ang
            best = (x, y)
    if best:
        print(f"{best[0]:.5f} {best[1]:.5f}")

if __name__ == "__main__":
    main()