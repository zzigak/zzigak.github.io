# ########## PROGRAM: node_11:cc_python_11 ##########

from codebank import *

def main():
    x1, y1, r1 = map(int, input().split())
    x2, y2, r2 = map(int, input().split())
    x3, y3, r3 = map(int, input().split())
    k1, p1 = apollonius(x1, y1, r1, x2, y2, r2)
    k2, p2 = apollonius(x1, y1, r1, x3, y3, r3)
    # ensure if one is line it is k1
    if k1 != 'line' and k2 == 'line':
        k1, k2 = k2, k1
        p1, p2 = p2, p1
    candidates = []
    if k1 == 'line' and k2 == 'line':
        pt = intersect_lines(p1, p2)
        if pt: candidates = [pt]
    elif k1 == 'line' and k2 == 'circle':
        a, b, c = p1
        candidates = line_circle_intersections(a, b, c, *p2)
    elif k1 == 'circle' and k2 == 'circle':
        candidates = circle_intersections(p1, p2)
    # choose best by angle
    if not candidates:
        return
    best = max(candidates, key=lambda P: get_angle(x1, y1, r1, P[0], P[1]))
    print(f"{best[0]:.5f} {best[1]:.5f}")

if __name__ == "__main__":
    main()