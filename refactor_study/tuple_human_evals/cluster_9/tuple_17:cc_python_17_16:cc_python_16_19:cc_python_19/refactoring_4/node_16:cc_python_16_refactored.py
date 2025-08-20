from codebank import *

def main():
    n, m = read_ints()
    edges = []
    for _ in range(m):
        u, v, w = read_ints()
        edges.append((u-1, v-1, w))
    adj = build_adj_list(n, edges)
    dist = two_step_dijkstra(adj)
    INF = 10**18
    for i in range(n):
        if dist[i] >= INF:
            dist[i] = -1
    print(" ".join(map(str, dist)))

if __name__ == "__main__":
    main()