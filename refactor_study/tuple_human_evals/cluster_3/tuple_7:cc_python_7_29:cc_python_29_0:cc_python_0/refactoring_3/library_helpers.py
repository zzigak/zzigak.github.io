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
    adj = [[] for _ in range(n)]
    for _ in range(n-1):
        u, v = read_ints()
        if offset == 0:
            u -= 1; v -= 1
        adj[u].append(v)
        adj[v].append(u)
    return adj

def parorder(adj, root=0):
    par = [0]*len(adj)
    par[root] = -1
    stk = [root]
    order = []
    seen = {root}
    while stk:
        u = stk.pop()
        order.append(u)
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                par[v] = u
                stk.append(v)
    return par, order

def tree_reroot(adj, weights, root=0):
    par, order = parorder(adj, root)
    n = len(adj)
    dp = [0]*n
    for u in reversed(order):
        s = 0
        for v in adj[u]:
            if v != par[u]:
                s += max(0, dp[v])
        dp[u] = weights[u] + s
    res = [0]*n
    res[root] = dp[root]
    for u in order:
        if u != root:
            p = par[u]
            res[u] = dp[u] + max(0, res[p] - max(0, dp[u]))
    return res

def tree_dp_balance(adj, vals, root=0):
    par, order = parorder(adj, root)
    n = len(adj)
    plus = [0]*n
    minus = [0]*n
    for u in reversed(order):
        for v in adj[u]:
            if v != par[u]:
                plus[u] = max(plus[u], plus[v])
                minus[u] = max(minus[u], minus[v])
        val = vals[u] + minus[u] - plus[u]
        if val > 0:
            plus[u] += val
        else:
            minus[u] -= val
    return plus[root] + minus[root]

def can_satisfy(b, a, parents, ks):
    n = len(b)
    diff = [b[i] - a[i] for i in range(n)]
    for i in range(n-1, 0, -1):
        p = parents[i]
        if diff[i] >= 0:
            diff[p] += diff[i]
        else:
            diff[p] += diff[i] * ks[i]
        if diff[p] < 0:
            return False
    return diff[0] >= 0
