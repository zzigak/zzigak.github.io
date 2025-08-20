from codebank import *

def main():
    n = read_int()
    if n % 2:
        print(-1)
        return
    edges = [(u-1, v-1) for u, v in (read_ints() for _ in range(n-1))]
    adj = build_undirected_adj(n, edges)
    print(count_even_cuts(adj))

if __name__ == "__main__":
    main()