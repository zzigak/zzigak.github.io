from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n, m, s, t = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(m)]
    und, edge_set = build_undirected_graph(n, edges)
    ds = bfs(n, und, s-1)
    dt = bfs(n, und, t-1)
    target = ds[t-1]
    ans = count_nonconnect_pairs(n, edge_set, ds, dt, target)
    print(ans)

if __name__ == "__main__":
    main()