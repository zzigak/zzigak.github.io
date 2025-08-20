from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n, m = map(int, input().split())
    grid = [input().rstrip() for _ in range(n)]
    _ = list(map(int, input().split()))
    pos = []
    idx = [[-1]*m for _ in range(n)]
    for j in range(m):
        for i in range(n-1, -1, -1):
            if grid[i][j] == '#':
                idx[i][j] = len(pos)
                pos.append((i, j))
            elif i < n-1:
                idx[i][j] = idx[i+1][j]
    E = [[] for _ in pos]
    for k, (i, j) in enumerate(pos):
        if i+1 < n and idx[i+1][j] >= 0: E[k].append(idx[i+1][j])
        if i-1 >= 0 and grid[i-1][j] == '#': E[k].append(idx[i-1][j])
        if j-1 >= 0 and idx[i][j-1] >= 0: E[k].append(idx[i][j-1])
        if j+1 < m and idx[i][j+1] >= 0: E[k].append(idx[i][j+1])
    indeg_zero = scc_indeg_zero(E)
    print(sum(indeg_zero))

if __name__ == "__main__":
    main()