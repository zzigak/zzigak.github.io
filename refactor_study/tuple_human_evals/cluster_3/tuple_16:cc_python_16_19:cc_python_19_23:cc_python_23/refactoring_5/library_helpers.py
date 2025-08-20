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

def read_tree(n, offset=1):
    adj = [[] for _ in range(n)]
    for _ in range(n-1):
        u, v = read_ints()
        if offset:
            u -= 1; v -= 1
        adj[u].append(v)
        adj[v].append(u)
    return adj

def parorder(adj, root=0):
    par = [-1] * len(adj)
    par[root] = -1
    stack = [root]
    order = []
    visited = {root}
    while stack:
        u = stack.pop()
        order.append(u)
        for w in adj[u]:
            if w not in visited:
                visited.add(w)
                par[w] = u
                stack.append(w)
    return par, order

def get_children(par):
    children = [[] for _ in par]
    for u, p in enumerate(par):
        if p >= 0:
            children[p].append(u)
    return children

def compute_depth(par, order):
    depth = [0] * len(par)
    for u in order[1:]:
        depth[u] = depth[par[u]] + 1
    return depth

def compute_subtree_sizes(children, order):
    size = [0] * len(children)
    for u in reversed(order):
        tot = 0
        for c in children[u]:
            tot += size[c] + 1
        size[u] = tot
    return size

def maximize_beauty(L, R, adj):
    par, order = parorder(adj)
    children = get_children(par)
    n = len(adj)
    dp = [[0, 0] for _ in range(n)]
    for u in reversed(order):
        for c in children[u]:
            z0 = dp[c][0] + abs(L[u] - L[c])
            z1 = dp[c][1] + abs(L[u] - R[c])
            o0 = dp[c][0] + abs(R[u] - L[c])
            o1 = dp[c][1] + abs(R[u] - R[c])
            dp[u][0] += max(z0, z1)
            dp[u][1] += max(o0, o1)
    return max(dp[0])

def merge_dp(dp_v, dp_c, K, mod):
    m = max(len(dp_v), len(dp_c) + 1)
    res = [0] * m
    for i, dv in enumerate(dp_v):
        for j, dc in enumerate(dp_c):
            if i + j + 1 <= K:
                idx = max(i, j + 1)
                res[idx] = (res[idx] + dv * dc) % mod
            res[i] = (res[i] + dv * dc) % mod
    return res

def count_valid_subsets(adj, K, mod):
    par, order = parorder(adj)
    children = get_children(par)
    dp = [[1] for _ in adj]
    for u in reversed(order):
        for c in children[u]:
            dp[u] = merge_dp(dp[u], dp[c], K, mod)
    return sum(dp[0][:K+1]) % mod
