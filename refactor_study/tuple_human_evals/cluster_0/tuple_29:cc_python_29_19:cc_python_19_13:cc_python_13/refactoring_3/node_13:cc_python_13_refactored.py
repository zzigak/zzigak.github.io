import sys
from codebank import *

def main():
    input = sys.stdin.readline
    n = int(input())
    if n % 2:
        print(-1); return
    edges = [tuple(int(x)-1 for x in input().split()) for _ in range(n-1)]
    adj = build_undirected_graph(n, edges)
    order, parent = root_tree(adj, 0)
    init_vals = [1]*n
    subtree = aggregate_subtree(order, parent, init_vals, lambda a, b: a + b)
    res = sum(1 for i in range(1, n) if subtree[i] % 2 == 0)
    print(res)

if __name__ == "__main__":
    main()