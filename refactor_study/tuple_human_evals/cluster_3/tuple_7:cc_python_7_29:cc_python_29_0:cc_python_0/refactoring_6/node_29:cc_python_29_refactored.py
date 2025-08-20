from codebank import *

def main():
    n = int(input())
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = read_ints()
        u -= 1; v -= 1
        adj[u].append(v); adj[v].append(u)
    par, order = parorder(adj, 0)
    v = list(read_ints())
    plus = [0] * n
    minus = [0] * n
    for u in reversed(order):
        # adjust the value at u after children
        z = v[u] + plus[u] - minus[u]
        if z > 0:
            minus[u] += z
        else:
            plus[u] += -z
        p = par[u]
        if p >= 0:
            plus[p] = max(plus[p], plus[u])
            minus[p] = max(minus[p], minus[u])
    # root is 0
    print(plus[0] + minus[0])

if __name__ == "__main__":
    main()