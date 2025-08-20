from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n, m = map(int, input().split())
    edges_per_color = {}
    for _ in range(m):
        u, v, c = map(int, input().split())
        u -= 1; v -= 1
        edges_per_color.setdefault(c, []).append((u, v))
    comp_per_color = {}
    for c, edges in edges_per_color.items():
        adj, _ = build_adj_list(n, edges), None
        comp, _ = connected_components(adj)
        comp_per_color[c] = comp
    q = int(input())
    for _ in range(q):
        u, v = map(int, input().split())
        u -= 1; v -= 1
        ans = 0
        for comp in comp_per_color.values():
            if comp[u] == comp[v]:
                ans += 1
        print(ans)

if __name__ == "__main__":
    main()