from codebank import *

def main():
    n, m = read_ints()
    edges = []
    for _ in range(m):
        u, v, w = read_ints()
        u -= 1; v -= 1
        edges.append((u, v, w))
    adj = build_adj_undirected(n, edges)
    dist, parent = dijkstra(adj, 0, n, dest=n-1)
    if dist[n-1] >= 10**30:
        print(-1)
    else:
        path = reconstruct_path(parent, 0, n-1)
        print(" ".join(map(str, path)))

if __name__ == "__main__":
    main()