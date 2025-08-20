from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    if n % 2:
        print(-1)
        return
    edges = [tuple(map(int, input().split())) for _ in range(n-1)]
    edges = [(u-1, v-1) for u, v in edges]
    adj = build_graph(n, edges, undirected=True)
    parent, order = dfs_parent_order(0, adj)
    sizes = compute_subtree_sizes(order, parent)
    res = max_even_cuts(sizes, parent)
    print(res)

if __name__ == "__main__":
    main()