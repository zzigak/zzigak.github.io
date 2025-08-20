from codebank import *

def main():
    n, m, s, t = map(int, input().split())
    s -= 1; t -= 1
    edges = []
    for _ in range(m):
        u, v = map(int, input().split())
        edges.append((u-1, v-1))
    adj = build_undir_graph(n, edges)
    ds = bfs_distance(adj, s)
    dt = bfs_distance(adj, t)
    d_st = ds[t]
    exist = [set() for _ in range(n)]
    for u, v in edges:
        exist[u].add(v)
        exist[v].add(u)
    ans = 0
    for u in range(n):
        for v in range(u+1, n):
            if v not in exist[u] and min(ds[u] + dt[v], dt[u] + ds[v]) + 1 >= d_st:
                ans += 1
    print(ans)

if __name__ == "__main__":
    main()