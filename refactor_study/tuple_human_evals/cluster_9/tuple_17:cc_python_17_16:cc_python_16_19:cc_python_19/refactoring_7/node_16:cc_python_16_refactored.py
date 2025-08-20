from codebank import *

def main():
    n, m = read_ints()
    edges = []
    for _ in range(m):
        u, v, w = read_ints()
        u -= 1; v -= 1
        edges.append((u, v, w))
    adj = build_adj_undirected(n, edges)
    def get_neighbors(u):
        for mid, w1 in adj[u]:
            for v, w2 in adj[mid]:
                yield v, (w1 + w2) ** 2
    dist = dijkstra_dynamic(n, 0, get_neighbors)
    res = [str(-1 if d >= 10**30 else int(d)) for d in dist]
    print(" ".join(res))

if __name__ == "__main__":
    main()