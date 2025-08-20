# ########## PROGRAM: node_13:cc_python_13 ##########

from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    if n % 2:
        print(-1)
        return
    edges = [tuple(int(x)-1 for x in input().split()) for _ in range(n-1)]
    adj = build_adj(n, edges)
    sz = [0]*n
    res = 0
    for u, p in iterative_postorder(adj):
        total = 1
        for v in adj[u]:
            if v != p:
                total += sz[v]
        sz[u] = total
        if p != -1 and total % 2 == 0:
            res += 1
    print(res)

if __name__ == "__main__":
    main()