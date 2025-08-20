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
import sys

def read_ints():
    return map(int, sys.stdin.readline().split())

def read_tree(n, offset=0):
    adj = [[] for _ in range(n + (1 if offset else 0))]
    for _ in range(n-1):
        u, v = list(read_ints())
        if offset==0:
            u -= 1; v -= 1
        adj[u].append(v)
        adj[v].append(u)
    return adj

def par_depth_order(adj, root=0):
    n = len(adj)
    par = [-1]*n
    depth = [0]*n
    order = []
    stack = [root]
    visited = [False]*n
    visited[root] = True
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                par[v] = u
                depth[v] = depth[u] + 1
                stack.append(v)
    return par, depth, order

def subtree_sizes(par, order):
    n = len(par)
    sz = [0]*n
    for u in reversed(order):
        p = par[u]
        if p != -1:
            sz[p] += sz[u] + 1
    return sz

def merge_dp(dp_v, dp_u, K):
    mod = 998244353
    m, n = len(dp_v), len(dp_u)
    res = [0] * max(m, n+1)
    for i in range(m):
        for j in range(n):
            prod = dp_v[i] * dp_u[j]
            if i + j + 1 <= K:
                idx = max(i, j+1)
                res[idx] = (res[idx] + prod) % mod
            res[i] = (res[i] + prod) % mod
    return res
