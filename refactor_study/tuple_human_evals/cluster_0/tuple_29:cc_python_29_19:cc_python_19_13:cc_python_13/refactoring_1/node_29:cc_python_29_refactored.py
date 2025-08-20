from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    colors = list(map(int, input().split()))
    edges = [tuple(int(x)-1 for x in input().split()) for _ in range(n-1)]
    adj = build_adj(n, edges)
    total_red = colors.count(1)
    total_blue = colors.count(2)
    subtree = [[0, 0] for _ in range(n)]
    ans = 0
    for u, p in iterative_postorder(adj):
        r = 0; b = 0
        for v in adj[u]:
            if v != p:
                cr, cb = subtree[v]
                r += cr; b += cb
                if (cr == total_red and cb == 0) or (cb == total_blue and cr == 0):
                    ans += 1
        if colors[u] == 1:
            r += 1
        elif colors[u] == 2:
            b += 1
        subtree[u] = [r, b]
    print(ans)

if __name__ == "__main__":
    main()