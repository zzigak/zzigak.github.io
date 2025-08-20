from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    colors = read_ints()
    edges = []
    for _ in range(n - 1):
        u, v = map(int, input().split())
        edges.append((u - 1, v - 1))
    adj = build_adj_list(n, edges)
    print(count_nice_edges(n, adj, colors))

if __name__ == "__main__":
    main()