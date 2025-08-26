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
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_3:cc_python_3 ##########

from codebank import sub_vec, add_vec, dist_sq, make_cube, match_vertices
from itertools import permutations, combinations

def main():
    import sys
    input = sys.stdin.readline
    raw = [list(map(int, input().split())) for _ in range(8)]
    orig = raw.copy()
    lines = raw.copy()
    # fix the last line as candidate q
    q_raw = lines.pop()
    # try all permutations of q_raw
    for perm_q in permutations(q_raw):
        q = list(perm_q)
        # choose any 3 of the remaining 7 lines as neighbors of q
        for i, j, k in combinations(range(7), 3):
            a_raw, b_raw, c_raw = lines[i], lines[j], lines[k]
            # permute each neighbor
            for perm_a in permutations(a_raw):
                x = list(perm_a)
                L2 = dist_sq(q, x)
                if L2 == 0:
                    continue
                for perm_b in permutations(b_raw):
                    y = list(perm_b)
                    if dist_sq(q, y) != L2 or dist_sq(x, y) != 2 * L2:
                        continue
                    for perm_c in permutations(c_raw):
                        z = list(perm_c)
                        if (dist_sq(q, z) != L2 or
                            dist_sq(x, z) != 2 * L2 or
                            dist_sq(y, z) != 2 * L2):
                            continue
                        verts = make_cube(q, x, y, z)
                        if match_vertices(verts, orig):
                            # assign each input line to one vertex
                            assigned = [None] * 8
                            assigned[7] = q
                            remaining = verts.copy()
                            for idx in range(7):
                                target = sorted(raw[idx])
                                for v in remaining:
                                    if sorted(v) == target:
                                        assigned[idx] = v
                                        remaining.remove(v)
                                        break
                            print("YES")
                            for v in assigned:
                                print(*v)
                            return
    print("NO")

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_8:cc_python_8 ##########

from codebank import sub_vec, dist_sq, collinear

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    # pts: list of (coords, original_index)
    pts = [(list(map(int, input().split())), i+1) for i in range(n)]
    p0, idx0 = pts[0]
    # find nearest neighbor to p0
    j = min(range(1, n), key=lambda i: dist_sq(pts[i][0], p0))
    p1, idx1 = pts[j]
    # find next point that is not collinear with p0,p1 and is closest to p0
    k = min(
        (i for i in range(1, n) if i != j and not collinear(p0, p1, pts[i][0])),
        key=lambda i: dist_sq(pts[i][0], p0)
    )
    p2, idx2 = pts[k]
    print(idx0, idx1, idx2)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_9:cc_python_9 ##########

from codebank import sub_vec, dot

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    pts = [list(map(int, input().split())) for _ in range(n)]
    # In 5D, there can be at most 2*d = 10 good points.
    if n > 11:
        print(0)
        return
    good = []
    for i, a in enumerate(pts):
        bad = False
        for j, b in enumerate(pts):
            if j == i: continue
            for k, c in enumerate(pts[j+1:], start=j+1):
                if k == i: continue
                # acute angle <=> dot((b-a),(c-a)) > 0
                if dot(sub_vec(b, a), sub_vec(c, a)) > 0:
                    bad = True
                    break
            if bad:
                break
        if not bad:
            good.append(i+1)
    print(len(good))
    print('\n'.join(map(str, good)))

if __name__ == "__main__":
    main()
