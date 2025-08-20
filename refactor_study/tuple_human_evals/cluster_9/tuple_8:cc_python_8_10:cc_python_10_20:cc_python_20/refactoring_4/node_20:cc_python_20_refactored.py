from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n, m, s = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(m)]
    adj = build_directed_graph(n, edges)
    order = dfs_postorder(n, adj)
    seen = [False] * n
    dfs_mark(s-1, adj, seen)
    cnt = 0
    for u in order:
        if not seen[u]:
            dfs_mark(u, adj, seen)
            cnt += 1
    print(cnt)

if __name__ == "__main__":
    main()