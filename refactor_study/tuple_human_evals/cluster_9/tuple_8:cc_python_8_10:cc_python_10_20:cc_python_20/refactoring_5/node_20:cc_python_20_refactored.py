from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n, m, s = map(int, input().split())
    s -= 1
    edges = [tuple(map(int, input().split())) for _ in range(m)]
    graph = build_graph(n, edges, False)
    order = dfs_fill_order(graph)
    seen = [False]*n
    dfs_mark(graph, s, seen)
    cnt = 0
    for u in order:
        if not seen[u]:
            dfs_mark(graph, u, seen)
            cnt += 1
    print(cnt)

if __name__ == "__main__":
    main()