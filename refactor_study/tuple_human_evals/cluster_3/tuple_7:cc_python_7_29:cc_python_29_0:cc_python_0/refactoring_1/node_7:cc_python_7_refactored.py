from codebank import read_ints, read_tree, parorder, get_children

def main():
    n = int(input())
    a = list(map(int, input().split()))
    weight = [0] + [1 if ai else -1 for ai in a]
    tree = read_tree(n, offset=1)
    par, order = parorder(tree, 1)
    children = get_children(par)
    dp = [0] * (n + 1)
    for u in reversed(order):
        tot = 0
        for v in children[u]:
            tot += max(dp[v], 0)
        dp[u] = weight[u] + tot
    res = [0] * (n + 1)
    res[1] = dp[1]
    for u in order[1:]:
        p = par[u]
        res[u] = dp[u] + max(res[p] - max(dp[u], 0), 0)
    print(*res[1:])

if __name__ == "__main__":
    main()