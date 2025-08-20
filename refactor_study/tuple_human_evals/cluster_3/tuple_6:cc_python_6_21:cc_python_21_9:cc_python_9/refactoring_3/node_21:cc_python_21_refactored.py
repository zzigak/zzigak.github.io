from codebank import *

def main():
    n = int(input())
    beaver = list(map(int, input().split()))
    adj = read_tree(n)
    start = int(input()) - 1
    par, order = parorder(adj, start)
    children = get_children(par)
    dp = [0]*n
    for u in reversed(order):
        reserve = 0 if par[u] == -1 else 1
        ch = children[u]
        ch_dp = [dp[v] for v in ch]
        ch_dp.sort(reverse=True)
        x = min(beaver[u] - reserve, len(ch))
        dp_u = (0 if reserve == 0 else 1) + sum(ch_dp[:x]) + x
        beaver[u] -= x + reserve
        for v in ch:
            pairs = min(beaver[u], beaver[v])
            beaver[u] -= pairs
            dp_u += 2*pairs
        dp[u] = dp_u
    print(dp[start])

if __name__ == "__main__":
    main()