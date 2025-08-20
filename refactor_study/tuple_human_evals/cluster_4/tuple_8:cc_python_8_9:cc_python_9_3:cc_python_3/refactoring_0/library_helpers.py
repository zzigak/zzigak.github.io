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
from itertools import permutations
from collections import Counter

def sub(p, q):
    """Vector subtraction for arbitrary dimensions."""
    return tuple(pi - qi for pi, qi in zip(p, q))

def dot(p, q):
    """Dot product for arbitrary dimensions."""
    return sum(pi * qi for pi, qi in zip(p, q))

def norm_sq(p):
    """Squared Euclidean norm."""
    return dot(p, p)

def cross(p, q):
    """2D cross product (scalar)."""
    return p[0] * q[1] - p[1] * q[0]

def collinear(p, q, r):
    """Check if points p, q, r are collinear in the plane."""
    return cross(sub(q, p), sub(r, p)) == 0

def generate_cube_vertices(q, x, y, z):
    """Given three orthogonal neighbors x,y,z of q, generate all 8 cube vertices."""
    f = lambda a, b: tuple(ai + bi - qi for ai, bi, qi in zip(a, b, q))
    ab = f(x, y)
    ac = f(x, z)
    bc = f(y, z)
    abc = f(ab, z)
    return [q, x, y, z, ab, ac, bc, abc]

def triples_counter(triples):
    """Count sorted triples as a multiset."""
    return Counter(tuple(sorted(triple)) for triple in triples)
