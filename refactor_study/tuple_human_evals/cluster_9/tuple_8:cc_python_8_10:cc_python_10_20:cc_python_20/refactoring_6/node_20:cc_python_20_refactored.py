from codebank import *

def main():
    import sys
    sys.setrecursionlimit(10000)
    input = sys.stdin.readline
    n, m, s = map(int, input().split())
    s -= 1
    edges = [tuple(int(x)-1 for x in input().split()) for _ in range(m)]
    g = build_adj_directed(n, edges)
    order = dfs_finish_order(g)
    visited = [False]*n
    dfs_mark(s, g, visited)
    cnt = 0
    for u in reversed(order):
        if not visited[u]:
            dfs_mark(u, g, visited)
            cnt += 1
    print(cnt)

if __name__ == "__main__":
    main()