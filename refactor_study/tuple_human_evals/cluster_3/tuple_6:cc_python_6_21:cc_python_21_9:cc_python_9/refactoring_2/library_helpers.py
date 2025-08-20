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
def read_ints():
    return list(map(int, input().split()))

def read_tree(n, offset=0):
    adj = [[] for _ in range(n + (1 if offset else 0))]
    for _ in range(n - 1):
        u, v = read_ints()
        if offset == 0:
            u -= 1; v -= 1
        adj[u].append(v)
        adj[v].append(u)
    return adj

def read_weighted_tree(n, offset=0):
    adj = [[] for _ in range(n + (1 if offset else 0))]
    for _ in range(n - 1):
        u, v, c = read_ints()
        if offset == 0:
            u -= 1; v -= 1
        adj[u].append((v, c))
        adj[v].append((u, c))
    return adj

def parorder(adj, root):
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

def postorder(adj, root=0):
    n = len(adj)
    par = [-1] * n
    order = []
    stack = [(root, -1, False)]
    while stack:
        u, p, done = stack.pop()
        if not done:
            par[u] = p
            stack.append((u, p, True))
            for v in adj[u]:
                if v != p:
                    stack.append((v, u, False))
        else:
            order.append(u)
    return par, order
