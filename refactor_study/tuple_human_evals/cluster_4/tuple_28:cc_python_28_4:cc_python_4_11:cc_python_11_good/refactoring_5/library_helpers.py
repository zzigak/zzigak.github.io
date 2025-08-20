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

def normalize_direction(dx, dy):
    """Reduce (dx,dy) to primitive integer direction with canonical sign."""
    g = gcd(abs(dx), abs(dy))
    dx //= g
    dy //= g
    if dx < 0 or (dx == 0 and dy < 0):
        dx = -dx
        dy = -dy
    return dx, dy

def intersect_line_line(line1, line2):
    """Intersect two lines given as (a,b,c): ax+by+c=0."""
    a1, b1, c1 = line1
    a2, b2, c2 = line2
    d = a1*b2 - a2*b1
    if abs(d) < 1e-12:
        return []
    x = (b1*c2 - b2*c1)/d
    y = (c1*a2 - c2*a1)/d
    return [(x, y)]

def line_circle_intersections(a, b, c, xc, yc, r):
    """Intersection points between line ax+by+c=0 and circle center(xc,yc), radius r."""
    d2 = a*a + b*b
    if d2 == 0:
        return []
    # signed distance from center to line
    f = a*xc + b*yc + c
    # foot of perpendicular
    x0 = xc - a*f/d2
    y0 = yc - b*f/d2
    h2 = r*r - f*f/d2
    if h2 < -1e-12:
        return []
    if abs(h2) < 1e-12:
        return [(x0, y0)]
    h = sqrt(h2/d2)
    dx = -b*h
    dy = a*h
    return [(x0+dx, y0+dy), (x0-dx, y0-dy)]

def circle_intersections(c1, c2):
    """Return intersection points between two circles (x1,y1,r1),(x2,y2,r2)."""
    x1, y1, r1 = c1
    x2, y2, r2 = c2
    dx = x2 - x1
    dy = y2 - y1
    d = hypot(dx, dy)
    if d == 0 or d > r1 + r2 or d < abs(r1 - r2):
        return []
    a = (r1*r1 - r2*r2 + d*d) / (2*d)
    h2 = r1*r1 - a*a
    h = sqrt(h2) if h2 > 0 else 0.0
    ux = dx/d
    uy = dy/d
    x3 = x1 + a*ux
    y3 = y1 + a*uy
    if h == 0:
        return [(x3, y3)]
    rx = -uy*h
    ry = ux*h
    return [(x3+rx, y3+ry), (x3-rx, y3-ry)]

def locus_between_circles(c1, c2):
    """Locus where two circles are seen at same angle: returns ('line',a,b,c) or ('circle',cx,cy,r)."""
    x1, y1, r1 = c1
    x2, y2, r2 = c2
    if abs(r1 - r2) < 1e-12:
        # perpendicular bisector
        mx = (x1 + x2)/2
        my = (y1 + y2)/2
        a = x2 - x1
        b = y2 - y1
        c = -(a*mx + b*my)
        return ('line', a, b, c)
    # Apollonian circle
    c_ratio = (r1*r1) / (r2*r2)
    cx = (c_ratio*x2 - x1)/(c_ratio - 1)
    cy = (c_ratio*y2 - y1)/(c_ratio - 1)
    d2 = (x1 - x2)**2 + (y1 - y2)**2
    r = sqrt(c_ratio * d2 / ((c_ratio - 1)**2))
    return ('circle', cx, cy, r)

def intersect_shapes(s1, s2):
    """Intersect two loci: each is ('line',...) or ('circle',...)."""
    t1 = s1[0]; t2 = s2[0]
    if t1 == 'line' and t2 == 'line':
        return intersect_line_line(s1[1:], s2[1:])
    if t1 == 'line' and t2 == 'circle':
        return line_circle_intersections(*s1[1:], *s2[1:])
    if t1 == 'circle' and t2 == 'line':
        return line_circle_intersections(*s2[1:], *s1[1:])
    return circle_intersections(s1[1:], s2[1:])

def get_view_angle(xc, yc, r, x, y):
    """Return half of the apparent angle of circle from (x,y)."""
    d = hypot(x - xc, y - yc)
    return asin(r/d) if d != 0 else 0.0
