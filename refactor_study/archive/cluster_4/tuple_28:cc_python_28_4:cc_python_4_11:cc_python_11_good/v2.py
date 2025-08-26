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
from itertools import combinations
from math import gcd, sqrt, hypot, asin

def group_lines(points):
    """Group unique infinite lines by normalized direction and intercept."""
    groups = {}
    for (x1, y1), (x2, y2) in combinations(points, 2):
        dx, dy = x2 - x1, y2 - y1
        dir = normalize_direction(dx, dy)
        # normal n = (dy, -dx) ⇒ intercept C = n·p = dy*x1 - dx*y1
        C = dir[1] * x1 - dir[0] * y1
        groups.setdefault(dir, set()).add(C)
    return groups

def count_intersections(groups):
    """Count intersecting pairs among all unique lines."""
    sizes = [len(s) for s in groups.values()]
    total = sum(sizes)
    res = 0
    for sz in sizes:
        res += sz * (total - sz)
    return res // 2

def perpendicular_bisector(p1, p2):
    """Return (a,b,c) for perpendicular bisector ax+by+c=0 of segment p1-p2."""
    x1, y1 = p1; x2, y2 = p2
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    # bisector normal is (dx, dy)
    a, b = dx, dy
    c = -(a * mx + b * my)
    return (a, b, c)

def apollonian_circle(c1, c2):
    """Return (cx,cy,r) of Apollonian circle for circles c1,c2."""
    x1, y1, r1 = c1; x2, y2, r2 = c2
    k = r1 * r1 / (r2 * r2)
    cx = (k * x2 - x1) / (k - 1)
    cy = (k * y2 - y1) / (k - 1)
    r = abs(r1) * sqrt(((x1 - x2)**2 + (y1 - y2)**2) / (k - 1)**2)
    return (cx, cy, r)

def locus_equal_angle(c1, c2):
    """Return ('line',a,b,c) or ('circle',x,y,r) for equal-angle locus."""
    if c1[2] == c2[2]:
        return ('line', *perpendicular_bisector((c1[0], c1[1]), (c2[0], c2[1])))
    else:
        return ('circle', *apollonian_circle(c1, c2))

def intersect_loci(l1, l2):
    """Intersect two loci: line-line, line-circle or circle-circle."""
    tp1 = l1[0]; tp2 = l2[0]
    if tp1 == 'line' and tp2 == 'line':
        _, a1, b1, c1 = l1; _, a2, b2, c2 = l2
        det = a1*b2 - a2*b1
        if abs(det) < 1e-9: return []
        x = (-c1*b2 + c2*b1)/det
        y = (a2*c1 - a1*c2)/det
        return [(x, y)]
    if tp1 == 'circle' and tp2 == 'circle':
        _, x1, y1, r1 = l1; _, x2, y2, r2 = l2
        return circle_intersections((x1,y1,r1),(x2,y2,r2))
    # ensure l1 is line
    if tp1 == 'circle':
        l1, l2 = l2, l1; tp1, tp2 = tp2, tp1
    _, a, b, c = l1; _, cx, cy, r = l2
    # line ax+by+c=0 with circle center (cx,cy),r
    d = abs(a*cx + b*cy + c)/sqrt(a*a + b*b)
    if d > r: return []
    t = -(a*cx + b*cy + c)/(a*a + b*b)
    xp, yp = cx + a*t, cy + b*t
    h = sqrt(max(r*r - d*d,0)) / sqrt(a*a + b*b)
    dx, dy = -b, a
    x1, y1 = xp + dx*h, yp + dy*h
    if abs(h) < 1e-9:
        return [(x1, y1)]
    x2, y2 = xp - dx*h, yp - dy*h
    return [(x1, y1), (x2, y2)]

def get_viewing_angle(x, y, r, x0, y0):
    """Return the half-angle under which circle (x,y,r) is seen from (x0,y0)."""
    return asin(r / hypot(x0 - x, y0 - y))


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_11:cc_python_11 ##########

from codebank import *

def main():
    c1 = tuple(map(int, input().split()))
    c2 = tuple(map(int, input().split()))
    c3 = tuple(map(int, input().split()))
    locus12 = locus_equal_angle(c1, c2)
    locus13 = locus_equal_angle(c1, c3)
    pts = intersect_loci(locus12, locus13)
    best = None
    best_ang = -1
    for x, y in pts:
        ang = get_viewing_angle(c1[0], c1[1], c1[2], x, y)
        if ang > best_ang:
            best_ang = ang
            best = (x, y)
    if best:
        print(f"{best[0]:.5f} {best[1]:.5f}")

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_28:cc_python_28 ##########

from codebank import *

def main():
    n = int(input())
    points = [tuple(map(int, input().split())) for _ in range(n)]
    groups = group_lines(points)
    print(count_intersections(groups))

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_4:cc_python_4 ##########

from codebank import *

def main():
    n = int(input())
    points = [tuple(map(int, input().split())) for _ in range(n)]
    groups = group_lines(points)
    print(count_intersections(groups))

if __name__ == "__main__":
    main()
