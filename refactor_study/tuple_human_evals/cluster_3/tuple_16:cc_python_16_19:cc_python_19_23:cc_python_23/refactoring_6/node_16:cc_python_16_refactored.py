from codebank import *

def main():
    n, k = map(int, input().split())
    adj = read_tree(n)
    par, order = parorder(adj, 0)
    depth = [0] * n
    for u in order:
        if par[u] >= 0:
            depth[u] = depth[par[u]] + 1
    children = get_children(par)
    l = [0] * n
    for u in reversed(order):
        for v in children[u]:
            l[u] += l[v] + 1
    vals = [l[i] - depth[i] for i in range(n)]
    vals.sort(reverse=True)
    print(sum(vals[:n - k]))

if __name__ == "__main__":
    main()