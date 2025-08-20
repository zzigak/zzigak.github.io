from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        edges = [tuple(map(int, input().split())) for _ in range(n-1)]
        adj = build_adj_list(n, [(u-1,v-1) for u,v in edges])
        removes = []
        dfs_removals(0, -1, adj, removes, 0)
        for x, y in removes:
            adj[x].remove(y); adj[y].remove(x)
        ops = []
        l = find_leaf(0, adj)
        for x, y in removes:
            r = find_leaf(y, adj)
            ops.append((x+1, y+1, l+1, r+1))
            l = r
        out.append(str(len(ops)))
        for op in ops:
            out.append(" ".join(map(str, op)))
    print("\n".join(out))

if __name__ == "__main__":
    main()