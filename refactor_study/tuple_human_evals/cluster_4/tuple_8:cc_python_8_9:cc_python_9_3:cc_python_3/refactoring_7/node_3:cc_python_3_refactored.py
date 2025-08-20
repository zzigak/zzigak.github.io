from codebank import dist_sq, combine, sorted_multiset
from itertools import permutations

def main():
    import sys
    lines = sys.stdin.read().splitlines()
    orig = [tuple(map(int, line.split())) for line in lines]
    # sort each line's numbers to get the multiset
    sorted_sets = [tuple(sorted(p)) for p in orig]
    # pick the last as reference q
    q = tuple(sorted_sets.pop())
    target = sorted_multiset(sorted_sets)
    # try all choices of three distinct lines as the neighbors of q
    for a, b, c in permutations(sorted_sets, 3):
        for x in permutations(a):
            s = 2 * dist_sq(q, x)
            if s == 0:
                continue
            for y in permutations(b):
                if not (2 * dist_sq(q, y) == dist_sq(x, y) == s):
                    continue
                for z in permutations(c):
                    if not (2 * dist_sq(q, z) == dist_sq(x, z) == dist_sq(y, z) == s):
                        continue
                    # build the 7 other vertices
                    t = [
                        tuple(x),
                        tuple(y),
                        tuple(z),
                        combine(x, y, q),
                        combine(x, z, q),
                        combine(y, z, q),
                        combine(combine(x, y, q), z, q),
                    ]
                    if sorted_multiset(t) == target:
                        # success: assemble all 8 vertices
                        vertices = t + [q]
                        print("YES")
                        # print in the original input order
                        for orig_line in orig:
                            s_line = tuple(sorted(orig_line))
                            for i, v in enumerate(vertices):
                                if tuple(sorted(v)) == s_line:
                                    print(*v)
                                    vertices.pop(i)
                                    break
                        return
    print("NO")

if __name__ == "__main__":
    main()