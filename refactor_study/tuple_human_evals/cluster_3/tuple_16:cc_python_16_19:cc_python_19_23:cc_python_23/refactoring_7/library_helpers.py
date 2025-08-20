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
def read_ints():
    return map(int, input().split())

def read_tree(n, offset=0):
    adj = [[] for _ in range(n + (1 if offset else 0))]
    for _ in range(n - 1):
        u, v = read_ints()
        if offset == 0:
            u -= 1; v -= 1
        adj[u].append(v)
        adj[v].append(u)
    return adj

def parorder(adj, root):
    par = [-1] * len(adj)
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
    return par, order

def get_children(par):
    children = [[] for _ in par]
    for u, p in enumerate(par):
        if p >= 0:
            children[p].append(u)
    return children

def compute_depth_and_subtree(adj, root):
    n = len(adj)
    parent = [-1] * n
    depth = [0] * n
    sizes = [0] * n
    stack = [root]
    order = []
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            depth[v] = depth[u] + 1
            stack.append(v)
    for u in reversed(order):
        for v in adj[u]:
            if v != parent[u]:
                sizes[u] += sizes[v] + 1
    return depth, sizes

def compute_beauty(L, R, adj, root=0):
    par, order = parorder(adj, root)
    n = len(adj)
    dp0 = [0] * n
    dp1 = [0] * n
    for u in reversed(order):
        if u == root:
            continue
        p = par[u]
        zero = max(dp0[u] + abs(L[p] - L[u]), dp1[u] + abs(L[p] - R[u]))
        one  = max(dp0[u] + abs(R[p] - L[u]), dp1[u] + abs(R[p] - R[u]))
        dp0[p] += zero
        dp1[p] += one
    return max(dp0[root], dp1[root])

def compute_valid_sets(adj, K, mod):
    par, order = parorder(adj, 0)
    children = get_children(par)
    dp = [[1] for _ in range(len(adj))]
    for v in reversed(order):
        for u in children[v]:
            dv, du = dp[v], dp[u]
            len_v, len_u = len(dv), len(du)
            new_len = max(len_v, len_u + 1)
            res_dp = [0] * new_len
            for i in range(len_v):
                for j in range(len_u):
                    prod = dv[i] * du[j] % mod
                    if i + j + 1 <= K:
                        idx = max(i, j + 1)
                        res_dp[idx] = (res_dp[idx] + prod) % mod
                    res_dp[i] = (res_dp[i] + prod) % mod
            dp[v] = res_dp
    return sum(dp[0][i] for i in range(min(K + 1, len(dp[0])))) % mod
