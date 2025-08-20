from codebank import *
from fractions import Fraction
import sys
sys.setrecursionlimit(10**7)

def main():
    n = int(sys.stdin.readline())
    adj = [[] for _ in range(n)]
    for _ in range(n-1):
        u, v = map(int, sys.stdin.readline().split())
        u -= 1; v -= 1
        adj[u].append(v)
        adj[v].append(u)
    parent, post = dfs_postorder(adj, 0)
    children = [[] for _ in range(n)]
    for v, p in enumerate(parent):
        if p >= 0:
            children[p].append(v)
    H = [0] * n
    F = [0] * n
    FoH = [None] * n
    for u in post:
        F[u] = 1
        rat = []
        for v in children[u]:
            F[u] *= H[v]
            rat.append(Fraction(F[v], H[v]))
        FoH[u] = sorted(rat, reverse=True)
        ans = F[u]
        pd = 1
        for i, x in enumerate(FoH[u], 1):
            pd *= x
            ans = max(ans, int(pd * F[u]) * (i+1))
        for v in children[u]:
            pd = 1
            for i, x in enumerate(FoH[v], 1):
                pd *= x
                val = int(pd * F[u] * F[v]) // H[v] * (i+2)
                if val > ans:
                    ans = val
        H[u] = ans
    print(H[0])

if __name__ == "__main__":
    main()