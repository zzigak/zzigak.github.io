from codebank import *

def main():
    n, m = read_ints()
    edges = []
    for _ in range(m):
        u, v, w = read_ints()
        edges.append((u-1, v-1, w))
    adj = build_adj_list(n, edges)
    path = shortest_path(adj, 0, n-1)
    if path is None:
        print(-1)
    else:
        print(" ".join(map(str, path)))

if __name__ == "__main__":
    main()