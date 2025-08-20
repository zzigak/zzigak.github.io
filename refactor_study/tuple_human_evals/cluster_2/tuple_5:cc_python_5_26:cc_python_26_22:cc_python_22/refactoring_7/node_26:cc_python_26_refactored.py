from codebank import *

def main():
    import sys
    sys.setrecursionlimit(10**7)
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        n = int(input())
        edges = []
        for _ in range(n-1):
            a, b = map(int, input().split())
            edges.append((a-1, b-1))
        adj = build_adj_list(n, edges)
        removals = []
        collect_removals(0, -1, adj, removals)
        # cut the collected edges
        for u, v in removals:
            adj[u].remove(v)
            adj[v].remove(u)
        ops = []
        l = find_leaf(0, adj)
        for u, v in removals:
            r = find_leaf(v, adj)
            # convert back to 1-based
            ops.append((u+1, v+1, l+1, r+1))
            l = find_leaf(r, adj)
        print(len(ops))
        for x, y, x2, y2 in ops:
            print(x, y, x2, y2)

if __name__ == "__main__":
    main()