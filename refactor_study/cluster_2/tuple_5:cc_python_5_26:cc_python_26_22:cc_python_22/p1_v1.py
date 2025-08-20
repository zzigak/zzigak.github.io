# ########## PROGRAM: node_22:cc_python_22 ##########

from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    N, M = map(int, input().split())
    grid = [input().rstrip() for _ in range(N)]
    cnts = list(map(int, input().split()))  # read and ignore
    # index sand blocks
    id_map = [[-1]*M for _ in range(N)]
    I = []
    for j in range(M):
        for i in range(N-1, -1, -1):
            if grid[i][j] == '#':
                id_map[i][j] = len(I)
                I.append((i, j))
            elif i < N-1:
                id_map[i][j] = id_map[i+1][j]
    su = len(I)
    E = [[] for _ in range(su)]
    for k, (i, j) in enumerate(I):
        if i+1 < N and id_map[i+1][j] >= 0:
            E[k].append(id_map[i+1][j])
        if i-1 >= 0 and grid[i-1][j] == '#':
            E[k].append(id_map[i-1][j])
        if j-1 >= 0 and id_map[i][j-1] >= 0:
            E[k].append(id_map[i][j-1])
        if j+1 < M and id_map[i][j+1] >= 0:
            E[k].append(id_map[i][j+1])
    ciE = scc_ciE(E)
    print(sum(ciE))

if __name__ == "__main__":
    main()