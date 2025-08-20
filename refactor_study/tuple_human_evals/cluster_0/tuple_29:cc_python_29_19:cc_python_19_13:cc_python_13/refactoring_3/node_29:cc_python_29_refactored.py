import sys
from codebank import *

def main():
    input = sys.stdin.readline
    n = int(input())
    colors = list(map(int, input().split()))
    total_red = colors.count(1)
    total_blue = colors.count(2)
    edges = [tuple(int(x)-1 for x in input().split()) for _ in range(n-1)]
    adj = build_undirected_graph(n, edges)
    order, parent = root_tree(adj, 0)
    init_vals = [[1 if c==1 else 0, 1 if c==2 else 0] for c in colors]
    subtree = aggregate_subtree(order, parent, init_vals, lambda a, b: [a[0]+b[0], a[1]+b[1]])
    ans = sum(1 for i in range(1, n)
              if (subtree[i][0]==total_red and subtree[i][1]==0)
              or (subtree[i][1]==total_blue and subtree[i][0]==0))
    print(ans)

if __name__ == "__main__":
    main()