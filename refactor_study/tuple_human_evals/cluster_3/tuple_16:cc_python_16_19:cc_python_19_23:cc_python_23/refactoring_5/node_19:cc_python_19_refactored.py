from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        n = int(input())
        L = []
        R = []
        for _ in range(n):
            l, r = map(int, input().split())
            L.append(l)
            R.append(r)
        adj = [[] for _ in range(n)]
        for _ in range(n-1):
            u, v = map(int, input().split())
            u -= 1; v -= 1
            adj[u].append(v)
            adj[v].append(u)
        print(maximize_beauty(L, R, adj))

if __name__ == "__main__":
    main()