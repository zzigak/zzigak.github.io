# ########## LIBRARY HELPERS ##########

# ==== RETRIEVED HELPER FUNCTIONS ====

# Selected Helper Functions

from itertools import combinations
from collections import defaultdict

def normalize_direction(dx, dy):
    """Reduce (dx,dy) to primitive integer direction with canonical sign."""
    # Selected because: We need to group lines by their direction (slope) in a
    # canonical integer form to detect and count unique infinite lines.
    g = gcd(abs(dx), abs(dy))
    dx //= g
    dy //= g
    if dx < 0 or (dx == 0 and dy < 0):
        dx = -dx
        dy = -dy
    return (dx, dy)


# Selected Helper Functions

# Selected because: We need to normalize direction vectors to uniquely identify slopes of lines
from math import gcd

def line_between(p, q):
    """
    Returns (a, b, c) for the line ax + by + c = 0 through points p and q.
    Selected because: get_line(p1, p2) in the plan needs a robust way to form a line.
    """
    a = p[1] - q[1]
    b = q[0] - p[0]
    c = p[0] * q[1] - p[1] * q[0]
    return (a, b, c)

def line_eval(line, p):
    """
    Evaluates ax + by + c for line=(a,b,c) at point p.
    Selected because: get_points(a,b,c,x,y,r) needs to compute distance from
    circle center to the line and the foot of perpendicular.
    """
    (a, b, c) = line
    return a * p[0] + b * p[1] + c

def circle_intersections(c1, c2):
    """
    Return list of intersection points between two circles (x1,y1,r1) and (x2,y2,r2).
    Selected because: in the plan, when comm() yields two circles, their intersections
    give candidate observation points.
    """
    (x1, y1, r1) = c1
    (x2, y2, r2) = c2
    dx, dy = x2 - x1, y2 - y1
    d = hypot(dx, dy)
    if d == 0 or d > r1 + r2 or d < abs(r1 - r2):
        return []
    # distance from c1 to line through intersection points
    a = (r1*r1 - r2*r2 + d*d) / (2*d)
    h_sq = r1*r1 - a*a
    h = sqrt(h_sq) if h_sq > 0 else 0.0
    ux, uy = dx / d, dy / d
    x3, y3 = x1 + a*ux, y1 + a*uy
    if h == 0:
        return [(x3, y3)]
    rx, ry = -uy*h, ux*h
    return [(x3 + rx, y3 + ry), (x3 - rx, y3 - ry)]


# ==== NEW HELPER FUNCTIONS ====
from math import gcd, sqrt, hypot, asin

def compute_line_key(p, q):
    x1, y1 = p; x2, y2 = q
    dx, dy = x2 - x1, y2 - y1
    dir = normalize_direction(dx, dy)
    nx, ny = -dir[1], dir[0]
    c = nx * x1 + ny * y1
    return dir, c

def apollonius(x1, y1, r1, x2, y2, r2):
    if r1 == r2:
        a = x2 - x1; b = y2 - y1
        mx = (x1 + x2) / 2; my = (y1 + y2) / 2
        c = -(a * mx + b * my)
        return 'line', (a, b, c)
    c_ratio = (r1 * r1) / (r2 * r2)
    cx = (c_ratio * x2 - x1) / (c_ratio - 1)
    cy = (c_ratio * y2 - y1) / (c_ratio - 1)
    R = sqrt((c_ratio * ((x1 - x2) ** 2 + (y1 - y2) ** 2)) / ((c_ratio - 1) ** 2))
    return 'circle', (cx, cy, R)

def intersect_lines(l1, l2):
    a1, b1, c1 = l1; a2, b2, c2 = l2
    det = a1 * b2 - a2 * b1
    if abs(det) < 1e-12:
        return None
    x = (b1 * c2 - b2 * c1) / det
    y = (c1 * a2 - c2 * a1) / det
    return x, y

def line_circle_intersections(a, b, c, x0, y0, r):
    dist = abs(a * x0 + b * y0 + c) / sqrt(a*a + b*b)
    if dist > r:
        return []
    t = (a * x0 + b * y0 + c) / (a*a + b*b)
    xp = x0 - a * t; yp = y0 - b * t
    h = sqrt(max(r*r - dist*dist, 0)) / sqrt(a*a + b*b)
    if h < 1e-12:
        return [(xp, yp)]
    rx = -b * h; ry = a * h
    return [(xp + rx, yp + ry), (xp - rx, yp - ry)]

def get_angle(cx, cy, r, x, y):
    return asin(r / hypot(x - cx, y - cy))


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

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

# ########## PROGRAM: node_28:cc_python_28 ##########

from codebank import *
from itertools import combinations
from collections import defaultdict

def main():
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]
    groups = defaultdict(set)
    for p, q in combinations(pts, 2):
        dir, c = compute_line_key(p, q)
        groups[dir].add(c)
    total = sum(len(v) for v in groups.values())
    res = 0
    for cnt in (len(v) for v in groups.values()):
        res += cnt * (total - cnt)
    print(res // 2)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_4:cc_python_4 ##########

from codebank import *
from itertools import combinations
from collections import defaultdict

def main():
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]
    groups = defaultdict(set)
    for p, q in combinations(pts, 2):
        dir, c = compute_line_key(p, q)
        groups[dir].add(c)
    total = sum(len(v) for v in groups.values())
    res = 0
    for cnt in (len(v) for v in groups.values()):
        res += cnt * (total - cnt)
    print(res // 2)

if __name__ == "__main__":
    main()
