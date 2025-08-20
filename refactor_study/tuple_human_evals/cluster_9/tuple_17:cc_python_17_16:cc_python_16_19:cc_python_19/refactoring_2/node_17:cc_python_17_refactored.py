from codebank import *

def main():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v, w = map(int, input().split())
        edges.append((u-1, v-1, w))
    adj = build_undirected_adj(n, edges)
    dist, parent = dijkstra(adj, 0)
    path = reconstruct_path(parent, 0, n-1)
    if not path:
        print(-1)
    else:
        print(" ".join(str(v+1) for v in path))

if __name__ == "__main__":
    main()