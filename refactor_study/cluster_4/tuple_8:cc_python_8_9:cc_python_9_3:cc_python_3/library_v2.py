# ########## LIBRARY HELPERS ##########

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

def sub_vec(a, b):
    """Subtracts vectors component-wise."""
    return [x - y for x, y in zip(a, b)]

def add_vec(a, b):
    """Adds vectors component-wise."""
    return [x + y for x, y in zip(a, b)]

def dist_sq(a, b):
    """Squared Euclidean distance between points a and b."""
    return sum((x - y) ** 2 for x, y in zip(a, b))

def make_cube(q, x, y, z):
    """
    Given one vertex q of a cube and its three neighbors x,y,z,
    returns all eight cube vertices.
    """
    v_xy = sub_vec(add_vec(x, y), q)
    v_xz = sub_vec(add_vec(x, z), q)
    v_yz = sub_vec(add_vec(y, z), q)
    v_xyz = sub_vec(sub_vec(add_vec(add_vec(x, y), z), q), q)
    return [q, x, y, z, v_xy, v_xz, v_yz, v_xyz]

def match_vertices(generated, original):
    """
    Checks multiset equality of generated vs original points,
    ignoring order within each triple.
    """
    gen = Counter(tuple(sorted(v)) for v in generated)
    orig = Counter(tuple(sorted(v)) for v in original)
    return gen == orig


# ########################################
#
