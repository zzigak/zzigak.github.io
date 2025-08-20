from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        n = int(input())
        edges = [tuple(x-1 for x in map(int, input().split())) for _ in range(n-1)]
        adj = build_adj_list(n, edges)
        bad = []
        mark_bad_edges(0, -1, adj, bad)
        for u, v in bad:
            adj[u].remove(v)
            adj[v].remove(u)
        res = []
        leaf_prev = bfs_farthest(0, adj)
        for u, v in bad:
            r = bfs_farthest(v, adj)
            res.append((u, v, leaf_prev, r))
            leaf_prev = r
        print(len(res))
        for u, v, x, y in res:
            print(u+1, v+1, x+1, y+1)

if __name__ == "__main__":
    main()