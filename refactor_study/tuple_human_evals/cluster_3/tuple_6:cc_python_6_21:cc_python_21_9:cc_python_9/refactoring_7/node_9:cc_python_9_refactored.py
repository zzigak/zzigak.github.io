from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    adj = [[] for _ in range(n)]
    for _ in range(n-1):
        u, v = map(int, input().split())
        u -= 1; v -= 1
        adj[u].append(v)
        adj[v].append(u)
    print(max_product_components(adj, 0))

if __name__ == "__main__":
    main()