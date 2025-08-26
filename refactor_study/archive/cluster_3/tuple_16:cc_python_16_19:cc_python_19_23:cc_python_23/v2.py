# ########## LIBRARY HELPERS ##########

# ==== RETRIEVED HELPER FUNCTIONS ====
def parorder(adj, root):
    # Success rate: 6/6

    par = [0] * len(adj)
    par[root] = -1
    stack = [root]
    order = []
    visited = {root}
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if v not in visited:
                visited.add(v)
                par[v] = u
                stack.append(v)
    return (par, order)

def read_ints():
    # Success rate: 9/9

    return map(int, input().split())

def read_tree(n, offset=0):
    # Success rate: 7/7

    adj = [[] for _ in range(n + (1 if offset else 0))]
    for _ in range(n - 1):
        (u, v) = read_ints()
        if offset == 0:
            u -= 1
            v -= 1
        adj[u].append(v)
        adj[v].append(u)
    return adj

def get_children(par):
    # Success rate: 5/5

    children = [[] for _ in par]
    for (u, p) in enumerate(par):
        if p >= 0:
            children[p].append(u)
    return children


# ==== NEW HELPER FUNCTIONS ====

def merge_dp(dp_v, dp_c, K, mod):
    m = max(len(dp_v), len(dp_c) + 1)
    new = [0] * m
    for i, xv in enumerate(dp_v):
        for j, yv in enumerate(dp_c):
            prod = xv * yv % mod
            if i + j + 1 <= K:
                idx = max(i, j + 1)
                new[idx] = (new[idx] + prod) % mod
            new[i] = (new[i] + prod) % mod
    return new


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_16:cc_python_16 ##########

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

# ########## PROGRAM: node_19:cc_python_19 ##########

from codebank import *

def solve_case():
    n = int(input())
    L = [0] * n; R = [0] * n
    for i in range(n):
        L[i], R[i] = map(int, input().split())
    adj = read_tree(n)
    par, order = parorder(adj, 0)
    dp = [[0, 0] for _ in range(n)]
    for u in reversed(order):
        dp[u] = [0, 0]
        for v in adj[u]:
            if v == par[u]: continue
            dp0 = max(dp[v][0] + abs(L[u] - L[v]),
                      dp[v][1] + abs(L[u] - R[v]))
            dp1 = max(dp[v][0] + abs(R[u] - L[v]),
                      dp[v][1] + abs(R[u] - R[v]))
            dp[u][0] += dp0
            dp[u][1] += dp1
    return max(dp[0])

def main():
    t = int(input())
    for _ in range(t):
        print(solve_case())

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_23:cc_python_23 ##########

from codebank import *

def main():
    mod = 998244353
    n, K = map(int, input().split())
    adj = read_tree(n)
    par, order = parorder(adj, 0)
    children = get_children(par)
    dp = [[1] for _ in range(n)]
    for u in reversed(order):
        for c in children[u]:
            dp[u] = merge_dp(dp[u], dp[c], K, mod)
    print(sum(dp[0][:K+1]) % mod)

if __name__ == "__main__":
    main()
