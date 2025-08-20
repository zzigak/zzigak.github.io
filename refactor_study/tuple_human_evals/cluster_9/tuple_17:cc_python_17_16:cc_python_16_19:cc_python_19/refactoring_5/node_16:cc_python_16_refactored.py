from codebank import *

def main():
    n, m = read_ints()
    edges = [(u-1, v-1, w) for u, v, w in (read_ints() for _ in range(m))]
    adj = build_adj_list(n, edges)
    dist = dijkstra_two_hop(n, adj, 0)
    INF = 10**24
    print(" ".join(str(int(d)) if d < INF else "-1" for d in dist))

if __name__ == "__main__":
    main()