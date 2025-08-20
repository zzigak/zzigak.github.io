from codebank import *
from itertools import permutations
from collections import defaultdict

def main():
    orig = [tuple(map(int, input().split())) for _ in range(8)]
    sorted_orig = [tuple(sorted(line)) for line in orig]
    q = orig[-1]
    q_sig = sorted_orig[-1]
    v_sigs = sorted_orig[:-1]
    u = sorted(v_sigs)
    m = len(v_sigs)
    for i in range(m):
        for j in range(i+1, m):
            for k in range(j+1, m):
                a_sig, b_sig, c_sig = v_sigs[i], v_sigs[j], v_sigs[k]
                for x in permutations(a_sig):
                    dx = norm_sq(sub(q, x))
                    if dx == 0:
                        continue
                    s = 2 * dx
                    for y in permutations(b_sig):
                        if norm_sq(sub(q, y)) * 2 != s or norm_sq(sub(x, y)) != s:
                            continue
                        for z in permutations(c_sig):
                            if norm_sq(sub(q, z)) * 2 != s:
                                continue
                            if norm_sq(sub(x, z)) != s or norm_sq(sub(y, z)) != s:
                                continue
                            # build all 8 vertices
                            v1 = add3(x, y, q)
                            v2 = add3(x, z, q)
                            v3 = add3(y, z, q)
                            v4 = add3(v1, z, q)
                            verts = [x, y, z, v1, v2, v3, v4, q]
                            sigs = [tuple(sorted(v)) for v in verts]
                            if sorted(sigs[:-1]) == u:
                                print("YES")
                                # map signatures to actual vertices
                                cand = defaultdict(list)
                                for vtx in verts:
                                    cand[tuple(sorted(vtx))].append(vtx)
                                # output in original order
                                for sig in sorted_orig:
                                    out = cand[sig].pop()
                                    print(*out)
                                return
    print("NO")

if __name__ == "__main__":
    main()