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

def normalize_direction(dx, dy):
    """Reduce (dx,dy) to primitive integer direction with canonical sign."""
    g = gcd(abs(dx), abs(dy))
    dx //= g
    dy //= g
    if dx < 0 or (dx == 0 and dy < 0):
        dx = -dx
        dy = -dy
    return (dx, dy)

# Selected because: We need to group lines by their direction and intercept
from collections import defaultdict

# Selected because: We must iterate over all pairs of points to enumerate lines
from itertools import combinations


# Selected Helper Functions

from math import sqrt, hypot

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
from itertools import combinations
from collections import defaultdict

def normalize_direction(dx, dy):
    g = gcd(abs(dx), abs(dy))
    dx //= g; dy //= g
    if dx < 0 or (dx == 0 and dy < 0):
        dx = -dx; dy = -dy
    return dx, dy

def get_lines(points):
    lines = defaultdict(set)
    for (x1, y1), (x2, y2) in combinations(points, 2):
        dx, dy = x2 - x1, y2 - y1
        dir = normalize_direction(dx, dy)
        ndx, ndy = dir
        c = ndy * x1 - ndx * y1
        lines[dir].add(c)
    return lines

def count_intersections(lines):
    total = sum(len(v) for v in lines.values())
    res = total * (total - 1) // 2
    for v in lines.values():
        k = len(v)
        res -= k * (k - 1) // 2
    return res

def get_locus(c1, c2):
    x1, y1, r1 = c1; x2, y2, r2 = c2
    if r1 == r2:
        a = x2 - x1; b = y2 - y1
        c = (x1*x1 + y1*y1 - x2*x2 - y2*y2) / 2
        return ('line', (a, b, c))
    k = r1*r1/(r2*r2)
    x = (k*x2 - x1)/(k - 1); y = (k*y2 - y1)/(k - 1)
    r = sqrt(k * ((x1 - x2)**2 + (y1 - y2)**2) / (k - 1)**2)
    return ('circle', (x, y, r))

def solve_line_line(L1, L2):
    a1, b1, c1 = L1; a2, b2, c2 = L2
    det = a1*b2 - a2*b1
    if abs(det) < 1e-9: return []
    x = (b1*c2 - b2*c1) / det
    y = (c1*a2 - c2*a1) / det
    return [(x, y)]

def solve_line_circle(line, circle):
    a, b, c = line; x0, y0, r = circle
    d = abs(a*x0 + b*y0 + c) / sqrt(a*a + b*b)
    if d > r + 1e-9: return []
    t = -(a*x0 + b*y0 + c) / (a*a + b*b)
    xh = x0 + a*t; yh = y0 + b*t
    if abs(d - r) < 1e-9: return [(xh, yh)]
    h = sqrt(r*r - d*d)
    norm = sqrt(a*a + b*b)
    ux = -b / norm; uy = a / norm
    return [(xh + ux*h, yh + uy*h), (xh - ux*h, yh - uy*h)]

def solve_circle_circle(c1, c2):
    x1, y1, r1 = c1; x2, y2, r2 = c2
    dx, dy = x2 - x1, y2 - y1
    d = hypot(dx, dy)
    if d < 1e-9 or d > r1 + r2 or d < abs(r1 - r2): return []
    a = (r1*r1 - r2*r2 + d*d) / (2*d)
    h2 = r1*r1 - a*a
    h = sqrt(h2) if h2 > 0 else 0.0
    ux, uy = dx / d, dy / d
    xm, ym = x1 + a*ux, y1 + a*uy
    if h < 1e-9: return [(xm, ym)]
    rx, ry = -uy*h, ux*h
    return [(xm + rx, ym + ry), (xm - rx, ym - ry)]

def intersect_locus(l1, l2):
    t1, v1 = l1; t2, v2 = l2
    if t1 == 'line' and t2 == 'line':
        return solve_line_line(v1, v2)
    if t1 == 'line' and t2 == 'circle':
        return solve_line_circle(v1, v2)
    if t1 == 'circle' and t2 == 'line':
        return solve_line_circle(v2, v1)
    return solve_circle_circle(v1, v2)

def get_angle(circle, point):
    x0, y0, r = circle; x, y = point
    d = hypot(x - x0, y - y0)
    if d <= r: return None
    return asin(r / d)
