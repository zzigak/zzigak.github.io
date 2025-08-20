from codebank import *

def main():
    n, m, s = map(int, input().split())
    s -= 1
    edges = [tuple(map(int, input().split())) for _ in range(m)]
    graph = build_graph(n, edges, False)
    li = compute_postorder(n, graph)
    visited = [False]*n
    dfs_mark(s, graph, visited)
    cnt = 0
    for u in li:
        if not visited[u]:
            dfs_mark(u, graph, visited)
            cnt += 1
    print(cnt)

if __name__ == "__main__":
    main()