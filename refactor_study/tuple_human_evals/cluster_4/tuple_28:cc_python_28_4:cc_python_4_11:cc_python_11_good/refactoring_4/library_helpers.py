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
from math import gcd, sqrt, asin

def normalize_direction(dx, dy):
    """Reduce (dx,dy) to primitive integer direction with canonical sign."""
    g = gcd(abs(dx), abs(dy))
    dx //= g
    dy //= g
    if dx < 0 or (dx == 0 and dy < 0):
        dx = -dx
        dy = -dy
    return (dx, dy)

def line_key(p, q):
    """Return direction and intercept key for line through p and q."""
    dx = q[0] - p[0]
    dy = q[1] - p[1]
    dir = normalize_direction(dx, dy)
    dxn, dyn = dir
    # normal vector = (-dyn, dxn)
    a = -dyn
    b = dxn
    c = -(a * p[0] + b * p[1])
    return dir, c

def get_apollonius(x1, y1, r1, x2, y2, r2):
    """Return Apollonius locus for two circles: ('line', (a,b,c)) or ('circle', (x,y,r))."""
    if r1 == r2:
        dx = x2 - x1
        dy = y2 - y1
        a = dx
        b = dy
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        c = -(a * mx + b * my)
        return 'line', (a, b, c)
    c = (r1 * r1) / (r2 * r2)
    x = (c * x2 - x1) / (c - 1)
    y = (c * y2 - y1) / (c - 1)
    dx = x1 - x2
    dy = y1 - y2
    r = sqrt(c * (dx * dx + dy * dy) / ((c - 1) ** 2))
    return 'circle', (x, y, r)

def intersect_lines(l1, l2):
    """Return intersection point of two lines ax+by+c=0, or None if parallel."""
    a1, b1, c1 = l1
    a2, b2, c2 = l2
    det = a1 * b2 - a2 * b1
    if abs(det) < 1e-12:
        return None
    x = (b1 * c2 - b2 * c1) / det
    y = (a2 * c1 - a1 * c2) / det
    return (x, y)

def intersect_line_circle(line, circle):
    """Return intersection points of line ax+by+c=0 and circle (cx,cy,r)."""
    a, b, c = line
    cx, cy, r = circle
    c0 = a * cx + b * cy + c
    A = a * a + b * b
    x0 = -a * c0 / A
    y0 = -b * c0 / A
    d2 = c0 * c0 / A
    if d2 > r * r:
        return []
    if abs(d2 - r * r) < 1e-12:
        return [(x0 + cx, y0 + cy)]
    h = sqrt((r * r - d2) / A)
    rx = b * h
    ry = -a * h
    return [(x0 + rx + cx, y0 + ry + cy),
            (x0 - rx + cx, y0 - ry + cy)]

def compute_angle(circle, point):
    """Return observation angle of circle at point."""
    cx, cy, r = circle
    dx = point[0] - cx
    dy = point[1] - cy
    dist = sqrt(dx * dx + dy * dy)
    return asin(r / dist)
