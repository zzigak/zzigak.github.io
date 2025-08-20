from codebank import build_adj_list, dfs_prune, find_leaf
import sys
sys.setrecursionlimit(10**7)

def main():
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        n = int(input())
        edges = [tuple(map(lambda x: int(x)-1, input().split())) for _ in range(n-1)]
        adj = build_adj_list(n, edges)
        removals = []
        dfs_prune(0, -1, adj, removals)
        for x, y in removals:
            adj[x].remove(y)
            adj[y].remove(x)
        ops = []
        l = find_leaf(0, adj)
        for p, y in removals:
            r = find_leaf(y, adj)
            ops.append((p+1, y+1, l+1, r+1))
            l = find_leaf(r, adj)
        print(len(ops))
        for x1, y1, x2, y2 in ops:
            print(x1, y1, x2, y2)

if __name__ == "__main__":
    main()