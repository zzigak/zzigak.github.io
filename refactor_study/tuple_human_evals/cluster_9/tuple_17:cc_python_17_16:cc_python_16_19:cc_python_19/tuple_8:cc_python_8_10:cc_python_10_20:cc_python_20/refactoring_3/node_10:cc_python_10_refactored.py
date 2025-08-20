from codebank import *

def main():
    n, m, s, t = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(m)]
    graph = build_adj_undirected(n, edges)
    ds = bfs_distance(graph, s-1)
    dt = bfs_distance(graph, t-1)
    target = ds[t-1]
    ans = 0
    for u in range(n):
        for v in range(u+1, n):
            if v not in graph[u] and min(ds[u] + dt[v], dt[u] + ds[v]) + 1 >= target:
                ans += 1
    print(ans)

if __name__ == "__main__":
    main()