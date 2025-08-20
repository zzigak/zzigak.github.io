from codebank import *

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        L = []; R = []
        for _ in range(n):
            l, r = read_ints()
            L.append(l); R.append(r)
        adj = read_tree(n)
        par, order = parorder(adj, 0)
        dp = [[0, 0] for _ in range(n)]
        for v in reversed(order):
            p = par[v]
            if p == -1:
                continue
            dp[p][0] += compute_contrib(dp[v], L[p], L[v], R[v])
            dp[p][1] += compute_contrib(dp[v], R[p], L[v], R[v])
        print(max(dp[0]))

if __name__ == "__main__":
    main()