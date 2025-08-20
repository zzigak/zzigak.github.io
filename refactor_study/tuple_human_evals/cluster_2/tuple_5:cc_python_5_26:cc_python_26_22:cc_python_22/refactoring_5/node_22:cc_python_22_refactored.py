from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n, m = map(int, input().split())
    grid = [input().rstrip() for _ in range(n)]
    # assign id to each block
    id_block = [[-1]*m for _ in range(n)]
    idx = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '#':
                id_block[i][j] = idx
                idx += 1
    if idx == 0:
        print(0)
        return
    # compute id_down: nearest block at or below for each cell
    id_down = [[-1]*m for _ in range(n)]
    for j in range(m):
        last = -1
        for i in range(n-1, -1, -1):
            if id_block[i][j] != -1:
                last = id_block[i][j]
            id_down[i][j] = last
    # build directed graph of disturbances
    E = [[] for _ in range(idx)]
    for i in range(n):
        for j in range(m):
            u = id_block[i][j]
            if u == -1:
                continue
            # fall to next block below
            if i+1 < n and id_down[i+1][j] != -1:
                E[u].append(id_down[i+1][j])
            # disturb block above at start
            if i-1 >= 0 and id_block[i-1][j] != -1:
                E[u].append(id_block[i-1][j])
            # disturb neighbor to the left along the fall
            if j-1 >= 0 and id_down[i][j-1] != -1:
                E[u].append(id_down[i][j-1])
            # disturb neighbor to the right along the fall
            if j+1 < m and id_down[i][j+1] != -1:
                E[u].append(id_down[i][j+1])
    # compute SCCs
    comp, cid = kosaraju_scc(E)
    indeg = [0]*cid
    for u in range(idx):
        cu = comp[u]
        for v in E[u]:
            cv = comp[v]
            if cu != cv:
                indeg[cv] += 1
    # count source components
    res = sum(1 for d in indeg if d == 0)
    print(res)

if __name__ == "__main__":
    main()