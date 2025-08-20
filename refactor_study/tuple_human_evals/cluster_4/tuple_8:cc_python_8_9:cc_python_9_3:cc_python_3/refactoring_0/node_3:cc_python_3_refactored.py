from codebank import *
from itertools import permutations, combinations

def main():
    lines = [tuple(map(int, input().split())) for _ in range(8)]
    target = triples_counter(lines)
    # try each line as the base vertex q
    for q_idx in range(8):
        for q in permutations(lines[q_idx]):
            other_idxs = [i for i in range(8) if i != q_idx]
            # pick any three to be the neighbors
            for i, j, k in combinations(other_idxs, 3):
                # iterate through permutations for x, y, z
                for x in permutations(lines[i]):
                    vqx = sub(x, q)
                    edge_sq = norm_sq(vqx)
                    if edge_sq == 0:
                        continue
                    for y in permutations(lines[j]):
                        vqy = sub(y, q)
                        if norm_sq(vqy) != edge_sq or dot(vqx, vqy) != 0:
                            continue
                        for z in permutations(lines[k]):
                            vqz = sub(z, q)
                            if (norm_sq(vqz) != edge_sq or
                                dot(vqx, vqz) != 0 or
                                dot(vqy, vqz) != 0):
                                continue
                            verts = generate_cube_vertices(q, x, y, z)
                            if triples_counter(verts) == target:
                                print("YES")
                                # assign vertices back to original lines
                                used = [False] * 8
                                out = [None] * 8
                                for idx in range(8):
                                    key = tuple(sorted(lines[idx]))
                                    for vidx, v in enumerate(verts):
                                        if not used[vidx] and tuple(sorted(v)) == key:
                                            used[vidx] = True
                                            out[idx] = v
                                            break
                                for v in out:
                                    print(*v)
                                return
    print("NO")

if __name__ == "__main__":
    main()