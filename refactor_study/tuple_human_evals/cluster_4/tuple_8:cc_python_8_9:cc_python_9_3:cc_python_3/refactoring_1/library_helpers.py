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
def sub(p, q):
    return tuple(pi - qi for pi, qi in zip(p, q))

def add(p, q):
    return tuple(pi + qi for pi, qi in zip(p, q))

def add3(a, b, c):
    return tuple(ai + bi - ci for ai, bi, ci in zip(a, b, c))

def dot(p, q):
    return sum(pi * qi for pi, qi in zip(p, q))

def norm_sq(p):
    return dot(p, p)

def cross(p, q):
    return p[0] * q[1] - p[1] * q[0]

def collinear(p, q, r):
    return cross(sub(q, p), sub(r, p)) == 0
