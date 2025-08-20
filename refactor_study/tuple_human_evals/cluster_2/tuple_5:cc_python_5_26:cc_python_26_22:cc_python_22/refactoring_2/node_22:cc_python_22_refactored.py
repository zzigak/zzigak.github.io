from codebank import scc_no_incoming

def main():
    import sys
    input = sys.stdin.readline
    N, M = map(int, input().split())
    grid = [input().rstrip() for _ in range(N)]
    a = list(map(int, input().split()))
    # assign block indices
    idx = [[-1]*M for _ in range(N)]
    positions = []
    cnt = 0
    for j in range(M):
        for i in range(N-1, -1, -1):
            if grid[i][j] == '#':
                idx[i][j] = cnt
                positions.append((i, j))
                cnt += 1
            elif i < N-1:
                idx[i][j] = idx[i+1][j]
    E = [[] for _ in range(cnt)]
    for k, (i, j) in enumerate(positions):
        if i+1 < N and idx[i+1][j] >= 0:
            E[k].append(idx[i+1][j])
        if i-1 >= 0 and grid[i-1][j] == '#':
            E[k].append(idx[i-1][j])
        if j-1 >= 0 and idx[i][j-1] >= 0:
            E[k].append(idx[i][j-1])
        if j+1 < M and idx[i][j+1] >= 0:
            E[k].append(idx[i][j+1])
    ciE = scc_no_incoming(E)
    print(sum(ciE))

if __name__ == "__main__":
    main()