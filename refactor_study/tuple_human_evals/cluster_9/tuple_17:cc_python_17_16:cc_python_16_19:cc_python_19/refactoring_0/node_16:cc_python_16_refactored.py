from codebank import *
import sys

def main():
    data = sys.stdin.readline().split()
    n, m = int(data[0]), int(data[1])
    edges = [tuple(map(int, sys.stdin.readline().split())) for _ in range(m)]
    edges = [(u-1, v-1, w) for u, v, w in edges]
    adj = build_adj_list(n, edges)
    dist = dijkstra_two_step(adj, 0)
    INF = 10**18
    for i in range(n):
        if dist[i] >= INF:
            dist[i] = -1
    print(" ".join(map(str, dist)))

if __name__ == "__main__":
    main()