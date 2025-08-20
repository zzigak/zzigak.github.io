from codebank import *
import sys

def main():
    data = sys.stdin.readline().split()
    n, m = int(data[0]), int(data[1])
    edges = [tuple(map(int, sys.stdin.readline().split())) for _ in range(m)]
    edges = [(u-1, v-1, w) for u, v, w in edges]
    adj = build_adj_list(n, edges)
    dist, parent = dijkstra(adj, 0)
    path = recover_path(parent, 0, n-1)
    print(-1 if not path else " ".join(map(str, path)))

if __name__ == "__main__":
    main()