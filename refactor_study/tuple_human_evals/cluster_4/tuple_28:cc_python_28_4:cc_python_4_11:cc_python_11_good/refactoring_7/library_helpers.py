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
from itertools import combinations
from collections import defaultdict
from math import gcd, sqrt, hypot

def normalize_direction(dx, dy):
    """Reduce (dx,dy) to primitive integer direction with canonical sign."""
    g = gcd(abs(dx), abs(dy))
    dx //= g; dy //= g
    if dx < 0 or (dx == 0 and dy < 0):
        dx = -dx; dy = -dy
    return dx, dy

def intersect_lines(l1, l2):
    """Intersection of two lines in form (a,b,c) for ax+by+c=0."""
    a1,b1,c1 = l1; a2,b2,c2 = l2
    det = a1*b2 - a2*b1
    if abs(det) < 1e-12:
        return []
    x = (b1*c2 - b2*c1)/det
    y = (c1*a2 - c2*a1)/det
    return [(x, y)]

def line_circle_intersection(line, circle):
    """Intersection points of line ax+by+c=0 with circle (x0,y0,r)."""
    a,b,c = line; x0,y0,r = circle
    D = a*a + b*b
    # projection of center onto line
    t = (a*x0 + b*y0 + c)/D
    fx = x0 - a*t; fy = y0 - b*t
    dist = abs(a*x0 + b*y0 + c)/sqrt(D)
    if dist > r + 1e-12:
        return []
    if abs(dist - r) < 1e-12:
        return [(fx, fy)]
    h = sqrt(r*r - dist*dist)
    ux, uy = b/sqrt(D), -a/sqrt(D)
    return [(fx + ux*h, fy + uy*h), (fx - ux*h, fy - uy*h)]

def circle_intersections(c1, c2):
    """Intersection points of two circles (x1,y1,r1) and (x2,y2,r2)."""
    x1,y1,r1 = c1; x2,y2,r2 = c2
    dx,dy = x2-x1, y2-y1
    d = hypot(dx, dy)
    if d == 0 or d > r1 + r2 or d < abs(r1 - r2):
        return []
    a = (r1*r1 - r2*r2 + d*d)/(2*d)
    h2 = r1*r1 - a*a
    h = sqrt(h2) if h2 > 0 else 0.0
    ux,uy = dx/d, dy/d
    x3,y3 = x1 + a*ux, y1 + a*uy
    if h == 0:
        return [(x3, y3)]
    rx,ry = -uy*h, ux*h
    return [(x3 + rx, y3 + ry), (x3 - rx, y3 - ry)]

def get_locus(c1, c2):
    """
    For circles c1=(x1,y1,r1), c2 returns
    ('line',(a,b,c)) if r1==r2 (perp. bisector)
    else ('circle',(cx,cy,R)) Apollonius circle.
    """
    x1,y1,r1 = c1; x2,y2,r2 = c2
    if r1 == r2:
        a = 2*(x2 - x1); b = 2*(y2 - y1)
        c = x1*x1 + y1*y1 - x2*x2 - y2*y2
        return ('line', (a, b, c))
    k2 = (r1/r2)**2
    denom = 1 - k2
    cx = (x1 - k2*x2)/denom
    cy = (y1 - k2*y2)/denom
    R = sqrt((cx - x1)**2 + (cy - y1)**2)
    return ('circle', (cx, cy, R))

def intersect_loci(l1, l2):
    """Intersect two loci from get_locus."""
    t1,p1 = l1; t2,p2 = l2
    if t1 == 'line' and t2 == 'line':
        return intersect_lines(p1, p2)
    if t1 == 'line' and t2 == 'circle':
        return line_circle_intersection(p1, p2)
    if t1 == 'circle' and t2 == 'line':
        return line_circle_intersection(p2, p1)
    # both circles
    return circle_intersections(p1, p2)
