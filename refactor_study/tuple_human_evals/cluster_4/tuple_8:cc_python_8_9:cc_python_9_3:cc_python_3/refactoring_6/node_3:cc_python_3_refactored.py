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