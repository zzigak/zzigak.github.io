from codebank import *

def main():
    n, m = read_ints()
    edges = [(u-1, v-1, w) for u, v, w in (read_ints() for _ in range(m))]
    adj = build_adj_list(n, edges)
    path = dijkstra_with_path(n, adj, 0, n-1)
    print(-1 if path is None else " ".join(map(str, path)))

if __name__ == "__main__":
    main()