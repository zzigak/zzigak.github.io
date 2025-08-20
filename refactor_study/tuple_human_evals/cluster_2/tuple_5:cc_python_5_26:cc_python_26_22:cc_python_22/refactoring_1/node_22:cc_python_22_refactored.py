from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n, m = map(int, input().split())
    Z = [input().rstrip() for _ in range(n)]
    idx = [[-1]*m for _ in range(n)]
    nodes = []
    for j in range(m):
        for i in range(n-1, -1, -1):
            if Z[i][j] == '#':
                idx[i][j] = len(nodes)
                nodes.append((i, j))
            elif i < n-1:
                idx[i][j] = idx[i+1][j]
    su = len(nodes)
    E = [[] for _ in range(su)]
    for k, (i, j) in enumerate(nodes):
        if i+1 < n and idx[i+1][j] >= 0:
            E[k].append(idx[i+1][j])
        if i-1 >= 0 and Z[i-1][j] == '#':
            E[k].append(idx[i-1][j])
        if j-1 >= 0 and idx[i][j-1] >= 0:
            E[k].append(idx[i][j-1])
        if j+1 < m and idx[i][j+1] >= 0:
            E[k].append(idx[i][j+1])
    ciE = scc(E)
    print(sum(ciE))

if __name__ == "__main__":
    main()