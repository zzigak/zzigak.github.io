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
    """Reduce (dx,dy) to primitive integer direction with canonical sign."""
    g = gcd(abs(dx), abs(dy))
    dx //= g; dy //= g
    if dx < 0 or (dx == 0 and dy < 0):
        dx = -dx; dy = -dy
    return dx, dy

def compute_intercept(direction, point):
    """Compute unique intercept for line with given direction through point."""
    dx, dy = direction
    x, y = point
    # normal vector is (-dy, dx), so c = a*x + b*y = -dy*x + dx*y
    return -dy * x + dx * y

def count_line_groups(points):
    """Return list of counts of distinct lines per slope."""
    lines = defaultdict(set)
    for (x1, y1), (x2, y2) in combinations(points, 2):
        d = normalize_direction(x2 - x1, y2 - y1)
        c = compute_intercept(d, (x1, y1))
        lines[d].add(c)
    return [len(s) for s in lines.values()]

def count_intersections(line_counts):
    """Given counts of lines in each slope group, return number of intersecting pairs."""
    total = sum(line_counts)
    sq = sum(c * c for c in line_counts)
    return (total * total - sq) // 2

def bisector(p1, p2):
    """Perpendicular bisector of p1-p2 as ('line', a, b, c) for a*x + b*y + c = 0."""
    dx = p2[0] - p1[0]; dy = p2[1] - p1[1]
    mx = (p1[0] + p2[0]) / 2; my = (p1[1] + p2[1]) / 2
    a, b = dx, dy
    c = -(a * mx + b * my)
    return ('line', a, b, c)

def apollonian_circle(p1, p2, r1, r2):
    """Apollonius circle for points p1,p2 with ratio of distances r1:r2."""
    c = r1 * r1 / (r2 * r2)
    x = (c * p2[0] - p1[0]) / (c - 1)
    y = (c * p2[1] - p1[1]) / (c - 1)
    R = sqrt((c * ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)) / ((c - 1)**2))
    return ('circle', x, y, R)

def intersect_line_line(l1, l2):
    """Intersection of two lines."""
    _, a1, b1, c1 = l1; _, a2, b2, c2 = l2
    det = a1 * b2 - a2 * b1
    if abs(det) < 1e-9:
        return []
    x = (b1 * c2 - b2 * c1) / det
    y = (a2 * c1 - a1 * c2) / det
    return [(x, y)]

def intersect_line_circle(line, circle):
    """Intersection points of a line and a circle."""
    _, a, b, c = line; _, x0, y0, R = circle
    d = abs(a * x0 + b * y0 + c) / sqrt(a * a + b * b)
    if d > R + 1e-9:
        return []
    t = (a * x0 + b * y0 + c) / (a * a + b * b)
    fx = x0 - a * t; fy = y0 - b * t
    if abs(d - R) < 1e-9:
        return [(fx, fy)]
    h = sqrt(R * R - d * d) / sqrt(a * a + b * b)
    rx = -b * h; ry = a * h
    return [(fx + rx, fy + ry), (fx - rx, fy - ry)]

def intersect_circle_circle(c1, c2):
    """Intersection points of two circles."""
    _, x1, y1, R1 = c1; _, x2, y2, R2 = c2
    dx = x2 - x1; dy = y2 - y1; d = hypot(dx, dy)
    if d > R1 + R2 or d < abs(R1 - R2) or d < 1e-9:
        return []
    a = (R1*R1 - R2*R2 + d*d) / (2 * d)
    h_sq = R1*R1 - a*a
    h = sqrt(h_sq) if h_sq > 0 else 0.0
    ux, uy = dx / d, dy / d
    mx = x1 + a * ux; my = y1 + a * uy
    if abs(h) < 1e-9:
        return [(mx, my)]
    rx = -uy * h; ry = ux * h
    return [(mx + rx, my + ry), (mx - rx, my - ry)]

def intersect(s1, s2):
    """Generic intersection dispatcher for line/circle shapes."""
    if s1[0] == 'line' and s2[0] == 'line':
        return intersect_line_line(s1, s2)
    if s1[0] == 'line' and s2[0] == 'circle':
        return intersect_line_circle(s1, s2)
    if s1[0] == 'circle' and s2[0] == 'line':
        return intersect_line_circle(s2, s1)
    if s1[0] == 'circle' and s2[0] == 'circle':
        return intersect_circle_circle(s1, s2)

def observation_angle(xc, yc, r, p):
    """Angle of observation of circle (xc,yc,r) from point p."""
    return asin(r / hypot(p[0] - xc, p[1] - yc))
