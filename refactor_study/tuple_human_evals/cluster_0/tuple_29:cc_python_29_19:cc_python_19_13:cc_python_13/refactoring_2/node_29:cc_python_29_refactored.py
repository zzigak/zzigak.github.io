from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))
    edges = [tuple(map(int, input().split())) for _ in range(n-1)]
    edges = [(u-1, v-1) for u, v in edges]
    adj = build_graph(n, edges, undirected=True)
    parent, order = dfs_parent_order(0, adj)
    node_values = [None] * n
    for i, col in enumerate(a):
        if col == 1:
            node_values[i] = 0
        elif col == 2:
            node_values[i] = 1
    total_counts = [a.count(1), a.count(2)]
    counts = compute_subtree_counts(order, parent, node_values, 2)
    ans = count_nice_edges(parent, counts, total_counts)
    print(ans)

if __name__ == "__main__":
    main()