from codebank import *

def main():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        v, u, w = map(int, input().split())
        edges.append((v-1, u-1, w))
    adj = build_undirected_adj(n, edges)
    dist = two_edge_dijkstra(adj)
    print(" ".join(str(d) for d in dist))

if __name__ == "__main__":
    main()