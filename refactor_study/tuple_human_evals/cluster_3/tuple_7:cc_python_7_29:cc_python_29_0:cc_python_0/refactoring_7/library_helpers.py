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

def read_tree(n):
    adj = [[] for _ in range(n)]
    for _ in range(n-1):
        u, v = read_ints()
        u -= 1; v -= 1
        adj[u].append(v); adj[v].append(u)
    return adj

def parorder(adj, root=0):
    par = [-1]*len(adj)
    stack = [root]; order = [ ]
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

def reroot_max_subtree(adj, vals):
    par, order = parorder(adj)
    children = get_children(par)
    n = len(adj)
    dp1 = [0]*n; dp2 = [0]*n
    for u in reversed(order):
        dp1[u] = vals[u]
        for v in children[u]:
            dp1[u] += max(0, dp1[v])
    for u in order:
        if par[u] == -1:
            dp2[u] = dp1[u]
        else:
            p = par[u]
            dp2[u] = dp1[u] + max(0, dp2[p] - max(0, dp1[u]))
    return dp2

def min_moves_to_zero(adj, vals):
    par, order = parorder(adj)
    children = get_children(par)
    n = len(adj)
    inc = [0]*n; dec = [0]*n
    for u in reversed(order):
        for v in children[u]:
            inc[u] = max(inc[u], inc[v])
            dec[u] = max(dec[u], dec[v])
        val = vals[u] + inc[u] - dec[u]
        if val > 0:
            dec[u] += val
        else:
            inc[u] += -val
    root = order[0]
    return inc[root] + dec[root]
