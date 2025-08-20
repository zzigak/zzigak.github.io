from codebank import *

def main():
    lines = [list(map(int, input().split())) for _ in range(8)]
    sorted_input = [tuple(sorted(line)) for line in lines]
    cnt_input = Counter(sorted_input)
    for i0 in range(8):
        for perm0 in permutations(lines[i0]):
            p0 = tuple(perm0)
            rem = [i for i in range(8) if i != i0]
            # choose three neighbors
            L = len(rem)
            for a in range(L):
                for b in range(a+1, L):
                    for c in range(b+1, L):
                        i1, i2, i3 = rem[a], rem[b], rem[c]
                        for perm1 in permutations(lines[i1]):
                            p1 = tuple(perm1)
                            v1 = sub(p1, p0)
                            if norm_sq(v1) == 0: continue
                            for perm2 in permutations(lines[i2]):
                                p2 = tuple(perm2)
                                v2 = sub(p2, p0)
                                if norm_sq(v2) != norm_sq(v1) or dot(v1, v2) != 0: continue
                                for perm3 in permutations(lines[i3]):
                                    p3 = tuple(perm3)
                                    v3 = sub(p3, p0)
                                    if norm_sq(v3) != norm_sq(v1): continue
                                    if dot(v1, v3) or dot(v2, v3): continue
                                    cube = make_cube(p0, v1, v2, v3)
                                    sorted_cube = [tuple(sorted(pt)) for pt in cube]
                                    if Counter(sorted_cube) == cnt_input:
                                        print("YES")
                                        unused = cube[:]
                                        for li in range(8):
                                            s = tuple(sorted(lines[li]))
                                            for j, up in enumerate(unused):
                                                if tuple(sorted(up)) == s:
                                                    print(*up)
                                                    unused.pop(j)
                                                    break
                                        return
    print("NO")

if __name__ == "__main__":
    main()