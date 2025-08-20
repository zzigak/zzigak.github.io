from codebank import *

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        L = [0]*n; R = [0]*n
        for i in range(n):
            L[i], R[i] = map(int, input().split())
        adj = read_tree(n)
        par, order = parorder(adj, 0)
        children = get_children(par)
        dp0 = [0]*n; dp1 = [0]*n
        for u in reversed(order):
            for v in children[u]:
                z = max(dp0[v] + abs(L[u]-L[v]), dp1[v] + abs(L[u]-R[v]))
                o = max(dp0[v] + abs(R[u]-L[v]), dp1[v] + abs(R[u]-R[v]))
                dp0[u] += z
                dp1[u] += o
        print(max(dp0[0], dp1[0]))

if __name__ == "__main__":
    main()