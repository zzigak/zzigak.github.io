from codebank import *

def main():
    n = int(input())
    adj = read_tree(n, offset=1)
    vals = [0] + list(map(int, input().split()))
    par, order = parorder(adj, 1)
    plus = [0] * (n + 1)
    minus = [0] * (n + 1)
    for u in reversed(order):
        # adjust current node after children's requirements
        cur = vals[u] + plus[u] - minus[u]
        if cur > 0:
            minus[u] += cur
        else:
            plus[u] -= cur
        p = par[u]
        if p != -1:
            plus[p] = max(plus[p], plus[u])
            minus[p] = max(minus[p], minus[u])
    print(plus[1] + minus[1])

if __name__ == "__main__":
    main()