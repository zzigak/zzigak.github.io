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
from collections import defaultdict
from itertools import combinations

def normalize_direction(dx, dy):
    """
    Reduce (dx,dy) to primitive integer direction with canonical sign.
    """
    g = gcd(abs(dx), abs(dy))
    dx //= g
    dy //= g
    if dx < 0 or (dx == 0 and dy < 0):
        dx = -dx
        dy = -dy
    return dx, dy

def intersect_lines(l1, l2):
    """
    Returns intersection point of two lines l1=(a,b,c), l2=(a,b,c),
    or None if they are parallel.
    """
    a1, b1, c1 = l1
    a2, b2, c2 = l2
    det = a1*b2 - a2*b1
    if abs(det) < 1e-12:
        return None
    x = (b1*c2 - b2*c1)/det
    y = (c1*a2 - c2*a1)/det
    return x, y

def line_circle_intersection(line, circle):
    """
    Returns list of intersection points between line (a,b,c) and circle (x0,y0,r).
    """
    a, b, c = line
    x0, y0, r = circle
    denom = a*a + b*b
    d = abs(a*x0 + b*y0 + c)/sqrt(denom)
    if d > r:
        return []
    t = (a*x0 + b*y0 + c)/denom
    xf = x0 - a*t
    yf = y0 - b*t
    if abs(d - r) < 1e-9:
        return [(xf, yf)]
    h = sqrt(r*r - d*d)
    norm = sqrt(denom)
    rx = -b*(h/norm)
    ry = a*(h/norm)
    return [(xf+rx, yf+ry), (xf-rx, yf-ry)]

def circle_circle_intersection(c1, c2):
    """
    Returns list of intersection points between circles c1 and c2.
    """
    x1, y1, r1 = c1
    x2, y2, r2 = c2
    dx = x2 - x1
    dy = y2 - y1
    d = hypot(dx, dy)
    if d == 0 or d > r1 + r2 or d < abs(r1 - r2):
        return []
    a = (r1*r1 - r2*r2 + d*d)/(2*d)
    h_sq = r1*r1 - a*a
    h = sqrt(h_sq) if h_sq > 0 else 0.0
    ux = dx/d
    uy = dy/d
    x3 = x1 + a*ux
    y3 = y1 + a*uy
    if h == 0:
        return [(x3, y3)]
    rx = -uy*h
    ry = ux*h
    return [(x3+rx, y3+ry), (x3-rx, y3-ry)]

def perpendicular_bisector(c1, c2):
    """
    Returns line (a,b,c) of perpendicular bisector of centers of c1 and c2.
    """
    x1, y1, _ = c1
    x2, y2, _ = c2
    a = 2*(x2 - x1)
    b = 2*(y2 - y1)
    c = x1*x1 + y1*y1 - x2*x2 - y2*y2
    return a, b, c

def apollonian_circle(c1, c2):
    """
    Returns Apollonian circle parameters (x,y,r) for c1 and c2.
    """
    x1, y1, r1 = c1
    x2, y2, r2 = c2
    ratio = (r1*r1)/(r2*r2)
    denom = ratio - 1.0
    x = (ratio*x2 - x1)/denom
    y = (ratio*y2 - y1)/denom
    r = sqrt((ratio*((x1-x2)**2 + (y1-y2)**2))/(denom*denom))
    return x, y, r

def angle_of_observation(circle, point):
    """
    Returns angle under which circle appears from point.
    """
    x, y, r = circle
    px, py = point
    return asin(r/hypot(px-x, py-y))
