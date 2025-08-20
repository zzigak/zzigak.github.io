# ########## LIBRARY HELPERS ##########

# ==== RETRIEVED HELPER FUNCTIONS ====
def read_tree(n, offset=0):
    # Success rate: 10/10

    adj = [[] for _ in range(n + (1 if offset else 0))]
    for _ in range(n - 1):
        (u, v) = read_ints()
        if offset == 0:
            u -= 1
            v -= 1
        adj[u].append(v)
        adj[v].append(u)
    return adj

def merge_dp(dp_v, dp_c, K, mod):
    # Success rate: 1/1

    m = max(len(dp_v), len(dp_c) + 1)
    new = [0] * m
    for (i, xv) in enumerate(dp_v):
        for (j, yv) in enumerate(dp_c):
            prod = xv * yv % mod
            if i + j + 1 <= K:
                idx = max(i, j + 1)
                new[idx] = (new[idx] + prod) % mod
            new[i] = (new[i] + prod) % mod
    return new

def parorder(adj, root):
    # Success rate: 9/9

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
    # Success rate: 12/12

    return map(int, input().split())

def get_children(par):
    # Success rate: 7/7

    children = [[] for _ in par]
    for (u, p) in enumerate(par):
        if p >= 0:
            children[p].append(u)
    return children


# ==== NEW HELPER FUNCTIONS ====
from collections import deque
from fractions import Fraction

def read_weighted_tree(n, offset=1):
    w = list(map(int, input().split()))
    adj = [[] for _ in range(n)]
    cost = {}
    for _ in range(n - 1):
        u, v, c = map(int, input().split())
        u -= offset; v -= offset
        adj[u].append(v); adj[v].append(u)
        cost[(u, v)] = c; cost[(v, u)] = c
    return w, adj, cost

def leaf_dp_max_gas(w, adj, cost):
    n = len(w)
    deg = [len(adj[i]) for i in range(n)]
    z = [[0] for _ in range(n)]
    stack = deque(i for i in range(n) if deg[i] == 1)
    while stack:
        x = stack.popleft()
        # y is the dp value for x
        y = max(z[x])
        deg[x] = 0
        for t in adj[x]:
            if deg[t] > 0:
                c = cost[(x, t)]
                z[t].append(y + w[x] - c)
                deg[t] -= 1
                if deg[t] == 1:
                    stack.append(t)
                break
    ans = 0
    for i in range(n):
        lst = sorted(z[i])
        best1 = lst[-1]
        ans = max(ans, w[i] + best1)
        if len(lst) >= 2:
            ans = max(ans, w[i] + best1 + lst[-2])
    return ans

def max_beavers_eaten(beaver, adj, start):
    n = len(adj)
    deg = [len(adj[i]) for i in range(n)]
    deg[start] += n
    dp = [0] * n
    stack = [i for i in range(n) if i != start and deg[i] == 1]
    while stack:
        v = stack.pop()
        deg[v] = 0
        child = []; child_dp = []
        for u in adj[v]:
            if deg[u] == 0:
                child.append(u); child_dp.append(dp[u])
            else:
                deg[u] -= 1
                if deg[u] == 1:
                    stack.append(u)
        child_dp.sort(reverse=True)
        x = min(beaver[v] - 1, len(child))
        if x < 0: x = 0
        dp[v] = 1 + sum(child_dp[:x]) + x
        beaver[v] -= x + 1
        for c in child:
            y = min(beaver[v], beaver[c])
            beaver[v] -= y
            dp[v] += 2 * y
    neigh_dp = sorted((dp[u] for u in adj[start]), reverse=True)
    x = min(beaver[start], len(adj[start]))
    ans = sum(neigh_dp[:x]) + x
    beaver[start] -= x
    for c in adj[start]:
        y = min(beaver[start], beaver[c])
        beaver[start] -= y
        ans += 2 * y
    return ans

def get_post_order(adj, root=0):
    n = len(adj)
    par = [-1] * n
    order = []
    stack = [(root, 0)]
    while stack:
        u, vis = stack.pop()
        if vis:
            order.append(u)
        else:
            stack.append((u, 1))
            for v in adj[u]:
                if v != par[u]:
                    par[v] = u
                    stack.append((v, 0))
    return order, par

def max_product_tree(adj):
    order, par = get_post_order(adj, 0)
    n = len(adj)
    F = [0] * n
    H = [0] * n
    FoH = [None] * n
    for u in order:
        F[u] = 1
        lst = []
        for v in adj[u]:
            if v != par[u]:
                F[u] *= H[v]
                lst.append(Fraction(F[v], H[v]))
        lst.sort(reverse=True)
        FoH[u] = lst
        ans = F[u]
        pd = Fraction(1, 1)
        for idx, x in enumerate(lst):
            pd *= x
            # merge idx+1 children
            ans = max(ans, int(pd * F[u]) * (idx + 2))
        for v in adj[u]:
            if v != par[u]:
                pd2 = Fraction(1, 1)
                for idx, x in enumerate(FoH[v]):
                    pd2 *= x
                    val = int(pd2 * F[u] * F[v]) // H[v] * (idx + 3)
                    ans = max(ans, val)
        H[u] = ans
    return H[0]


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_21:cc_python_21 ##########

from codebank import *

def main():
    n = int(input())
    beaver = list(map(int, input().split()))
    adj = read_tree(n)
    start = int(input()) - 1
    print(max_beavers_eaten(beaver, adj, start))

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_6:cc_python_6 ##########

from codebank import *

def main():
    n = int(input())
    w, adj, cost = read_weighted_tree(n)
    print(leaf_dp_max_gas(w, adj, cost))

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_9:cc_python_9 ##########

from codebank import *

def main():
    n = int(input())
    adj = read_tree(n)
    print(max_product_tree(adj))

if __name__ == "__main__":
    main()
