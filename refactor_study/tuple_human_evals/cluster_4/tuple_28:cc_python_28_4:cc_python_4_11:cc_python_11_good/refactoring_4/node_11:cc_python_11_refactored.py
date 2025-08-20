from codebank import *
import math

def main():
    x1, y1, r1 = map(int, input().split())
    x2, y2, r2 = map(int, input().split())
    x3, y3, r3 = map(int, input().split())
    c1 = (x1, y1, r1)
    # compute Apollonius loci for (c1,c2) and (c1,c3)
    type1, loc1 = get_apollonius(x1, y1, r1, x2, y2, r2)
    type2, loc2 = get_apollonius(x1, y1, r1, x3, y3, r3)
    # ensure first locus is line if either is a line
    if type1 == 'circle':
        type1, type2 = type2, type1
        loc1, loc2 = loc2, loc1
    if type1 == 'line' and type2 == 'line':
        pt = intersect_lines(loc1, loc2)
        if pt:
            print(f"{pt[0]:.5f} {pt[1]:.5f}")
    elif type1 == 'line' and type2 == 'circle':
        pts = intersect_line_circle(loc1, loc2)
        if pts:
            best = max(pts, key=lambda p: compute_angle(c1, p))
            print(f"{best[0]:.5f} {best[1]:.5f}")
    else:
        # both loci are circles
        x1p, y1p, r1p = loc1
        x2p, y2p, r2p = loc2
        a = 2 * (x1p - x2p)
        b = 2 * (y1p - y2p)
        c = (x2p*x2p + y2p*y2p - r2p*r2p) - (x1p*x1p + y1p*y1p - r1p*r1p)
        pts = intersect_line_circle((a, b, c), loc1)
        if pts:
            best = max(pts, key=lambda p: compute_angle(c1, p))
            print(f"{best[0]:.5f} {best[1]:.5f}")

if __name__ == "__main__":
    main()