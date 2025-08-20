from codebank import *

def main():
    n = read_int()
    colors = read_ints()
    edges = [(u-1, v-1) for u, v in (read_ints() for _ in range(n-1))]
    adj = build_undirected_adj(n, edges)
    print(count_nice_edges(adj, colors))

if __name__ == "__main__":
    main()