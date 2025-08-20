from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    from itertools import combinations, permutations

    # read the 8 scrambled rows
    rows = [tuple(map(int, input().split())) for _ in range(8)]
    sorted_rows = [sorted_tuple(r) for r in rows]
    # pick one as "q" (any vertex)
    v = sorted_rows.copy()
    q_sorted = v.pop()      # multiset of q's coords
    q = tuple(q_sorted)     # treat sorted order as the coordinate
    target = counter(v)     # desired multiset of the other 7 vertices

    # try any three of the remaining as adjacent to q
    for i, j, k in combinations(range(len(v)), 3):
        a_key, b_key, c_key = v[i], v[j], v[k]
        for x in permutations(a_key):
            s = 2 * sq_dist(q, x)
            if not s:
                continue
            for y in permutations(b_key):
                if not (2*sq_dist(q, y) == sq_dist(x, y) == s):
                    continue
                for z in permutations(c_key):
                    if not (2*sq_dist(q, z) == sq_dist(x, z) == s and sq_dist(y, z) == s):
                        continue
                    # generate the 7 other vertices
                    t = [
                        x, y, z,
                        add_sub(x, y, q),
                        add_sub(x, z, q),
                        add_sub(y, z, q),
                        add_sub(add_sub(x, y, q), z, q)
                    ]
                    if counter(tuple(sorted(pt)) for pt in t) == target:
                        print("YES")
                        # assign coordinates to each input row in order
                        printed_q = False
                        t_pts = t.copy()
                        for r in rows:
                            key = sorted_tuple(r)
                            if not printed_q and key == q_sorted:
                                print(*q)
                                printed_q = True
                            else:
                                # find matching point in t_pts
                                for idx, pt in enumerate(t_pts):
                                    if sorted_tuple(pt) == key:
                                        print(*pt)
                                        t_pts.pop(idx)
                                        break
                        return
    print("NO")

if __name__ == "__main__":
    main()