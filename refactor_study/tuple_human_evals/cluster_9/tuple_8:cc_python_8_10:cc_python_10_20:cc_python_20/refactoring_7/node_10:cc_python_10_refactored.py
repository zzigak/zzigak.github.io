from codebank import bfs_dist

def main():
    import sys
    input = sys.stdin.readline
    n, m, s, t = map(int, input().split())
    s -= 1; t -= 1
    graph = [set() for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1; v -= 1
        graph[u].add(v)
        graph[v].add(u)
    ds = bfs_dist(graph, s)
    dt = bfs_dist(graph, t)
    dist_st = ds[t]
    ans = 0
    for u in range(n):
        for v in range(u+1, n):
            if v not in graph[u] and min(ds[u] + dt[v], dt[u] + ds[v]) + 1 >= dist_st:
                ans += 1
    print(ans)

if __name__ == "__main__":
    main()