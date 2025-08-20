# ==== RETRIEVED HELPER FUNCTIONS ====

# Selected Helper Functions

# Selected because: We need vector subtraction to compute differences between points.
def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])

# Selected because: Used by norm_sq to compute the squared length of a vector.
def dot(p, q):
    return p[0] * q[0] + p[1] * q[1]

# Selected because: Computes squared length of a vector, allowing us to compare distances without sqrt.
def norm_sq(p):
    return dot(p, p)

# Selected because: We must test if three points are collinear (zero area).
def cross(p, q):
    return p[0] * q[1] - p[1] * q[0]

# Selected because: Directly implements the collinearity check via cross-product.
def collinear(p, q, r):
    return cross(sub(q, p), sub(r, p)) == 0


# Selected Helper Functions

def sub(p, q):
    """Vector subtraction: computes p - q component-wise."""
    return (p[0] - q[0], p[1] - q[1])

def dot(p, q):
    """Dot product: computes the scalar product of two vectors."""
    return p[0] * q[0] + p[1] * q[1]


# Selected Helper Functions

from collections import Counter

# Selected because:
# Counter will let us compare the multiset of candidate cube vertices
# (as tuples) against the multiset of input points efficiently,
# disregarding order.


# ==== NEW HELPER FUNCTIONS ====
from collections import Counter
from itertools import permutations

def sub(p, q):
    return tuple(pi - qi for pi, qi in zip(p, q))

def dot(p, q):
    return sum(pi * qi for pi, qi in zip(p, q))

def norm_sq(p):
    return dot(p, p)

def cross(p, q):
    return p[0] * q[1] - p[1] * q[0]

def collinear(p, q, r):
    return cross(sub(q, p), sub(r, p)) == 0

def add(p, q):
    return tuple(pi + qi for pi, qi in zip(p, q))

def make_cube(p0, v1, v2, v3):
    verts = []
    for m in range(8):
        cur = p0
        if m & 1: cur = add(cur, v1)
        if m & 2: cur = add(cur, v2)
        if m & 4: cur = add(cur, v3)
        verts.append(cur)
    return verts
