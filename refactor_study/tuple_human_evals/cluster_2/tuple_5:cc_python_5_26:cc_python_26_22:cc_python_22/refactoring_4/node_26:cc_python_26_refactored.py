from codebank import build_adj_list, collect_removals, find_leaf

def main():
    import sys
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        n = int(input())
        edges = [tuple(map(int, input().split())) for _ in range(n-1)]
        adj = build_adj_list(n+1, edges)
        removals = collect_removals(adj)
        for x, y in removals:
            adj[x].remove(y); adj[y].remove(x)
        ops = []
        l = find_leaf(1, adj)
        for x, y in removals:
            r = find_leaf(y, adj)
            ops.append((x, y, l, r))
            l = r
        print(len(ops))
        for x, y, a, b in ops:
            print(x, y, a, b)

if __name__ == "__main__":
    main()