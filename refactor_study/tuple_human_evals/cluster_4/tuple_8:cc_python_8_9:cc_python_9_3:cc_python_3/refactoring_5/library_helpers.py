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

def sub(p, q):
    """Vector subtraction in 2D."""
    return (p[0] - q[0], p[1] - q[1])

def dot(p, q):
    """Dot product in 2D."""
    return p[0] * q[0] + p[1] * q[1]

def norm_sq(p):
    """Squared length of a 2D vector."""
    return dot(p, p)

def cross(p, q):
    """2D cross product (scalar)."""
    return p[0] * q[1] - p[1] * q[0]

def collinear(p, q, r):
    """Check if three 2D points are collinear."""
    return cross(sub(q, p), sub(r, p)) == 0

def sub_nd(p, q):
    """Vector subtraction in N dimensions."""
    return tuple(pi - qi for pi, qi in zip(p, q))

def dot_nd(p, q):
    """Dot product in N dimensions."""
    return sum(pi * qi for pi, qi in zip(p, q))

def sq_dist(p, q):
    """Squared Euclidean distance in N dimensions."""
    return sum((pi - qi) ** 2 for pi, qi in zip(p, q))

def add_sub(p, q, r):
    """
    Compute p + q - r componentwise in N dimensions.
    Useful for cube-vertex generation.
    """
    return tuple(pi + qi - ri for pi, qi, ri in zip(p, q, r))

def sorted_tuple(p):
    """Return a tuple of the coordinates of p sorted ascending."""
    return tuple(sorted(p))

def counter(items):
    """Build a Counter (multiset) from the iterable items."""
    return Counter(items)
