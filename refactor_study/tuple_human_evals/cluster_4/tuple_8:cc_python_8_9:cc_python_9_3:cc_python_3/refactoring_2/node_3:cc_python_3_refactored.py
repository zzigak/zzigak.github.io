from codebank import *
import itertools

def main():
    lines = [list(map(int, input().split())) for _ in range(8)]
    sorted_lines = [tuple(sorted(line)) for line in lines]
    for qi in range(8):
        q = sorted_lines[qi]
        others = sorted_lines[:qi] + sorted_lines[qi+1:]
        multiset_others = sorted(others)
        for ia, ib, ic in itertools.permutations(range(7), 3):
            x, y, z = others[ia], others[ib], others[ic]
            dqx = dist_sq(q, x)
            if dqx == 0 or dist_sq(q, y) != dqx:
                continue
            s = 2 * dqx
            if dist_sq(x, y) != s:
                continue
            if dist_sq(q, z) != dqx or dist_sq(x, z) != s or dist_sq(y, z) != s:
                continue
            # construct the 8 cube vertices
            t = [
                x, y, z,
                sub(add(x, y), q),
                sub(add(x, z), q),
                sub(add(y, z), q),
                sub(add(sub(add(x, y), q), z), q)
            ]
            if sorted(t) == multiset_others:
                print("YES")
                candidates = t + [q]
                temp = candidates.copy()
                # assign each input line its matching point
                for sl in sorted_lines:
                    for j, p in enumerate(temp):
                        if tuple(sorted(p)) == sl:
                            print(*p)
                            temp.pop(j)
                            break
                return
    print("NO")

if __name__ == "__main__":
    main()