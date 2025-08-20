from codebank import build_adj_list, scc
def main():
    import sys
    input = sys.stdin.readline
    n, m = map(int, input().split())
    Z = [input().rstrip() for _ in range(n)]
    a = list(map(int, input().split()))
    # collect blocks
    I = []
    idx = [[-1]*m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if Z[i][j] == '#':
                idx[i][j] = len(I)
                I.append((i, j))
    total = len(I)
    edges = []
    # falling edges and horizontal adjacency along empty paths
    # preprocess blocks in each column
    cols = [[] for _ in range(m)]
    for k, (i, j) in enumerate(I):
        cols[j].append((i, k))
    for j in range(m):
        cols[j].sort()
        col = cols[j]
        L = len(col)
        for t in range(L):
            i, u = col[t]
            # next block row or bottom
            if t+1 < L:
                r2, v = col[t+1]
            else:
                r2, v = n, -1
            # falling edge to next block if exists
            if v >= 0:
                edges.append((u, v))
            # along empty cells between i and r2
            for r in range(i+1, r2):
                for nj in (j-1, j+1):
                    if 0 <= nj < m:
                        w = idx[r][nj]
                        if w >= 0:
                            edges.append((u, w))
    # adjacency edges for blocks at their cells
    for u, (i, j) in enumerate(I):
        for di, dj in ((-1,0),(1,0),(0,-1),(0,1)):
            ni, nj = i+di, j+dj
            if 0 <= ni < n and 0 <= nj < m:
                v = idx[ni][nj]
                if v >= 0:
                    edges.append((u, v))
    # build directed graph
    adj = build_adj_list(total, edges, directed=True)
    comp_id, comp_cnt = scc(adj)
    indeg = [0]*comp_cnt
    for u, v in edges:
        cu, cv = comp_id[u], comp_id[v]
        if cu != cv:
            indeg[cv] += 1
    # count source components
    ans = sum(1 for d in indeg if d == 0)
    print(ans)

if __name__ == "__main__":
    main()