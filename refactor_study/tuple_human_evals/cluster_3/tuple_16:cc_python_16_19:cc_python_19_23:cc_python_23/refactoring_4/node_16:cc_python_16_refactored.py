from codebank import *

def main():
    n, k = map(int, input().split())
    adj = read_tree(n)
    par, order = parorder(adj, 0)
    children = get_children(par)
    depth = [0] * n
    subtree = [1] * n
    for u in order[1:]:
        depth[u] = depth[par[u]] + 1
    for u in reversed(order):
        for v in children[u]:
            subtree[u] += subtree[v]
    vals = [depth[i] - (subtree[i] - 1) for i in range(n)]
    vals.sort(reverse=True)
    print(sum(vals[:k]))

if __name__ == "__main__":
    main()