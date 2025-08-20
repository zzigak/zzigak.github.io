# ==== RETRIEVED HELPER FUNCTIONS ====
def parorder(adj, root):
    # Success rate: 1/1

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
    # Success rate: 3/3

    return map(int, input().split())

def read_tree(n, offset=0):
    # Success rate: 3/3

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
    # Success rate: 1/1

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

def parorder(adj, root=0):
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
    return par, order

def get_children(par):
    children = [[] for _ in par]
    for u, p in enumerate(par):
        if p >= 0:
            children[p].append(u)
    return children

def compute_initial_dp(order, children, a):
    dp = [1 if a[i] == 1 else -1 for i in range(len(order))]
    for u in reversed(order):
        for v in children[u]:
            if dp[v] > 0:
                dp[u] += dp[v]
    return dp

def reroot_dp(u, children, dp, res):
    res[u] = dp[u]
    for v in children[u]:
        du, dv = dp[u], dp[v]
        if dv > 0:
            dp[u] -= dv
        if dp[u] > 0:
            dp[v] += dp[u]
        reroot_dp(v, children, dp, res)
        dp[u], dp[v] = du, dv

def compute_balances(order, children, vals):
    n = len(order)
    plus = [0] * n
    minus = [0] * n
    for u in reversed(order):
        for v in children[u]:
            plus[u] = max(plus[u], plus[v])
            minus[u] = max(minus[u], minus[v])
        t = vals[u] + minus[u] - plus[u]
        if t > 0:
            minus[u] += t
        else:
            plus[u] += -t
    return plus, minus

def compute_surplus(b, a):
    return [bi - ai for bi, ai in zip(b, a)]

def propagate_diff(diff, parents, ks):
    for i in range(len(diff) - 1, 0, -1):
        p = parents[i]
        if diff[i] >= 0:
            diff[p] += diff[i]
        else:
            diff[p] += diff[i] * ks[i]
    return diff[0]
