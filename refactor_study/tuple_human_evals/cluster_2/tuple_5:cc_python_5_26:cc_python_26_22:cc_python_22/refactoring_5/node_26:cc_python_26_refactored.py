from codebank import dfs_cuts, leaf

def main():
    import sys
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        n = int(input())
        adj = {i: [] for i in range(1, n+1)}
        for _i in range(n-1):
            a, b = map(int, input().split())
            adj[a].append(b)
            adj[b].append(a)
        cuts = []
        dfs_cuts(1, None, adj, set(), cuts)
        for x, y in cuts:
            adj[x].remove(y)
            adj[y].remove(x)
        ops = []
        l = leaf(1, adj)
        for p, y in cuts:
            r = leaf(y, adj)
            ops.append((p, y, l, r))
            l = leaf(r, adj)
        print(len(ops))
        for x1, y1, x2, y2 in ops:
            print(x1, y1, x2, y2)

if __name__ == "__main__":
    main()