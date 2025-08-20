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

def dist_sq(p, q):
    return norm_sq((p[0] - q[0], p[1] - q[1]))

def sub_general(p, q):
    return [pi - qi for pi, qi in zip(p, q)]

def dot_general(p, q):
    return sum(pi * qi for pi, qi in zip(p, q))


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_3:cc_python_3 ##########

from codebank import sub_general, dot_general
from itertools import permutations
from collections import Counter

def main():
    lines = [list(map(int, input().split())) for _ in range(8)]
    sorted_tr = [tuple(sorted(l)) for l in lines]
    cnt_tr = Counter(sorted_tr)
    for i0 in range(8):
        q = tuple(sorted(lines[i0]))
        for i1 in range(8):
            if i1 == i0: continue
            for i2 in range(8):
                if i2 in (i0, i1): continue
                for i3 in range(8):
                    if i3 in (i0, i1, i2): continue
                    for pa in permutations(lines[i1]):
                        a = pa
                        for pb in permutations(lines[i2]):
                            b = pb
                            for pc in permutations(lines[i3]):
                                c = pc
                                va = sub_general(a, q)
                                vb = sub_general(b, q)
                                vc = sub_general(c, q)
                                sq = dot_general(va, va)
                                if sq == 0 or dot_general(vb, vb) != sq or dot_general(vc, vc) != sq:
                                    continue
                                if dot_general(va, vb) != 0 or dot_general(va, vc) != 0 or dot_general(vb, vc) != 0:
                                    continue
                                v0 = q; v1 = a; v2 = b; v3 = c
                                v4 = tuple(v1[i] + v2[i] - v0[i] for i in range(3))
                                v5 = tuple(v1[i] + v3[i] - v0[i] for i in range(3))
                                v6 = tuple(v2[i] + v3[i] - v0[i] for i in range(3))
                                v7 = tuple(v1[i] + v2[i] + v3[i] - 2*v0[i] for i in range(3))
                                verts = [v0, v1, v2, v3, v4, v5, v6, v7]
                                sorted_verts = [tuple(sorted(v)) for v in verts]
                                if Counter(sorted_verts) != cnt_tr:
                                    continue
                                res = [None]*8
                                used = [False]*8
                                for idx in range(8):
                                    st = sorted_tr[idx]
                                    for j, v in enumerate(verts):
                                        if not used[j] and tuple(sorted(v)) == st:
                                            res[idx] = v
                                            used[j] = True
                                            break
                                print("YES")
                                for v in res:
                                    print(*v)
                                return
    print("NO")

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_8:cc_python_8 ##########

from codebank import *

def main():
    n = int(input())
    pts = [tuple(map(int, input().split())) + (i+1,)
           for i in range(n)]
    p0 = pts.pop()
    idx1, p1 = min(enumerate(pts),
                   key=lambda t: dist_sq(p0[:2], t[1][:2]))
    p1 = pts.pop(idx1)
    idx2, p2 = min(
        ((i, pt) for i, pt in enumerate(pts)
         if not collinear(p0[:2], p1[:2], pt[:2])),
        key=lambda t: dist_sq(p0[:2], t[1][:2])
    )
    p2 = pts[idx2]
    print(p0[2], p1[2], p2[2])

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_9:cc_python_9 ##########

from codebank import sub_general, dot_general

def main():
    n = int(input())
    pts = [list(map(int, input().split())) for _ in range(n)]
    good = []
    if n <= 11:
        for i, a in enumerate(pts):
            ok = True
            for j in range(n):
                if not ok:
                    break
                for k in range(j+1, n):
                    if j == i or k == i:
                        continue
                    v1 = sub_general(pts[j], a)
                    v2 = sub_general(pts[k], a)
                    if dot_general(v1, v2) > 0:
                        ok = False
                        break
            if ok:
                good.append(i+1)
    print(len(good))
    for idx in good:
        print(idx)

if __name__ == "__main__":
    main()
