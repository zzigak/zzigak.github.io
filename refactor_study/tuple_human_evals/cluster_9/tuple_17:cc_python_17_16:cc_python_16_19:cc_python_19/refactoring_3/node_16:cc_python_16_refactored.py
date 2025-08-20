from codebank import *

def main():
    n, m = read_ints()
    edges = []
    for _ in range(m):
        u, v, w = read_ints()
        edges.append((u-1, v-1, w))
    adj = build_undirected_graph(n, edges)
    dist = two_step_shortest(adj, n, 0)
    INF = 10**30
    res = [d if d < INF else -1 for d in dist]
    print(" ".join(map(str, res)))

if __name__ == "__main__":
    main()