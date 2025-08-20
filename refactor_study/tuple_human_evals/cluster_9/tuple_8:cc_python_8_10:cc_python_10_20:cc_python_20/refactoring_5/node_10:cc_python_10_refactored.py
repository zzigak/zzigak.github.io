from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n, m, s, t = map(int, input().split())
    s -= 1; t -= 1
    graph = [set() for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        graph[u-1].add(v-1)
        graph[v-1].add(u-1)
    adj = [list(neigh) for neigh in graph]
    ds = bfs(adj, s)
    dt = bfs(adj, t)
    Dst = ds[t]
    ans = 0
    for u in range(n):
        for v in range(u+1, n):
            if v not in graph[u] and min(ds[u] + dt[v], dt[u] + ds[v]) + 1 >= Dst:
                ans += 1
    print(ans)

if __name__ == "__main__":
    main()