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
        u, v = map(int, input().split())
        if offset == 0:
            u -= 1; v -= 1
        adj[u].append(v); adj[v].append(u)
    return adj

def parorder(adj, root):
    par = [-2] * len(adj)
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

def compute_dp1(adj, order, par, w):
    dp1 = w[:]  # dp1[u] = best subtree sum rooted at u
    for u in reversed(order):
        for v in adj[u]:
            if par[v] == u:
                dp1[u] += max(dp1[v], 0)
    return dp1

def compute_dp2(adj, order, par, dp1):
    dp2 = [0] * len(adj)
    root = order[0]
    dp2[root] = dp1[root]
    for u in order:
        for v in adj[u]:
            if par[v] == u:
                dp2[v] = dp1[v] + max(dp2[u] - max(dp1[v], 0), 0)
    return dp2

def compute_min_moves(adj, v, root=0):
    par, order = parorder(adj, root)
    n = len(adj)
    plus = [0] * n
    minus = [0] * n
    for u in reversed(order):
        if u == root: continue
        p = par[u]
        s = minus[u] - plus[u]
        z = v[u] + s
        plus[p] = max(plus[p], plus[u])
        minus[p] = max(minus[p], minus[u])
        if z > 0:
            plus[p] = max(plus[p], plus[u] + z)
        elif z < 0:
            minus[p] = max(minus[p], minus[u] - z)
    return plus[root] + minus[root]

def get_children(par):
    children = [[] for _ in par]
    for u, p in enumerate(par):
        if p >= 0:
            children[p].append(u)
    return children

def get_postorder(children, root):
    stack = [root]
    order = []
    while stack:
        u = stack.pop()
        order.append(u)
        for v in children[u]:
            stack.append(v)
    order.reverse()
    return order

def can_conduct_experiment(b, par, factor):
    children = get_children(par)
    post = get_postorder(children, 0)
    INF = 10**17
    for u in post:
        if u == 0: continue
        p = par[u]
        if b[u] >= 0:
            b[p] += b[u]
        else:
            b[p] += b[u] * factor[u]
            if b[p] < -INF:
                return False
    return b[0] >= 0
