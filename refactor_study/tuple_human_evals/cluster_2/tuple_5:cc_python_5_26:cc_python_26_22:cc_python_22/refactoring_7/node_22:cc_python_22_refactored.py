from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n, m = map(int, input().split())
    grid = [input().rstrip() for _ in range(n)]
    _ = list(map(int, input().split()))  # a_i, ignored since equals count
    # assign IDs to blocks
    id_grid = [[-1]*m for _ in range(n)]
    ids = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '#':
                id_grid[i][j] = ids
                ids += 1
    # build graph edges (down and right to avoid duplicates)
    edges = []
    for i in range(n):
        for j in range(m):
            u = id_grid[i][j]
            if u < 0:
                continue
            if i+1 < n and id_grid[i+1][j] >= 0:
                edges.append((u, id_grid[i+1][j]))
            if j+1 < m and id_grid[i][j+1] >= 0:
                edges.append((u, id_grid[i][j+1]))
    adj = build_adj_list(ids, edges)
    _, cid = connected_components(adj)
    print(cid)

if __name__ == "__main__":
    main()