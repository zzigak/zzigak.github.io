# ########## PROGRAM: node_22:cc_python_22 ##########

from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n, m = map(int, input().split())
    grid = [input().rstrip('\n') for _ in range(n)]
    ZZ = [[-1] * m for _ in range(n)]
    I = []
    for j in range(m):
        for i in range(n-1, -1, -1):
            if grid[i][j] == '#':
                ZZ[i][j] = len(I)
                I.append((i, j))
            elif i < n-1:
                ZZ[i][j] = ZZ[i+1][j]
    su = len(I)
    E = [[] for _ in range(su)]
    for k, (i, j) in enumerate(I):
        if i+1 < n and ZZ[i+1][j] >= 0:
            E[k].append(ZZ[i+1][j])
        if i-1 >= 0 and grid[i-1][j] == '#':
            E[k].append(ZZ[i-1][j])
        if j-1 >= 0 and ZZ[i][j-1] >= 0:
            E[k].append(ZZ[i][j-1])
        if j+1 < m and ZZ[i][j+1] >= 0:
            E[k].append(ZZ[i][j+1])
    print(compute_scc_zero_incoming(E))

if __name__ == "__main__":
    main()