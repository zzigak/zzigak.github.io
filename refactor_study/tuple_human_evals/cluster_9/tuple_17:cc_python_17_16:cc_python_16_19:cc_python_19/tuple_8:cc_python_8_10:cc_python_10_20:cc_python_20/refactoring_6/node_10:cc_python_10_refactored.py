from codebank import *

def main():
    n, m, s, t = map(int, input().split())
    s -= 1; t -= 1
    edges = [tuple(int(x)-1 for x in input().split()) for _ in range(m)]
    g = build_adj_undirected(n, edges)
    ds = bfs(s, g)
    dt = bfs(t, g)
    ans = 0
    D = ds[t]
    for u in range(n):
        for v in range(u+1, n):
            if v not in g[u] and min(ds[u] + dt[v], dt[u] + ds[v]) + 1 >= D:
                ans += 1
    print(ans)

if __name__ == "__main__":
    main()