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