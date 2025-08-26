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

def read_weighted_tree(n):
    adj = [[] for _ in range(n)]
    for _ in range(n-1):
        u, v, c = map(int, input().split())
        u -= 1; v -= 1
        adj[u].append((v, c))
        adj[v].append((u, c))
    return adj

def dfs_max(u, p, w, adj):
    best1 = best2 = 0
    max_sub = w[u]
    for v, cost in adj[u]:
        if v == p: continue
        down, sub = dfs_max(v, u, w, adj)
        if sub > max_sub:
            max_sub = sub
        contrib = down - cost
        if contrib > 0:
            if contrib > best1:
                best2, best1 = best1, contrib
            elif contrib > best2:
                best2 = contrib
    path_through = w[u] + best1 + best2
    if path_through > max_sub:
        max_sub = path_through
    return w[u] + best1, max_sub

def max_weighted_path(w, adj):
    return dfs_max(0, -1, w, adj)[1]

def prune_tree_parents(adj, start):
    n = len(adj)
    deg = [len(nb) for nb in adj]
    deg[start] += n
    stack = [i for i in range(n) if i != start and deg[i] == 1]
    order = []
    parent = [-1] * n
    while stack:
        v = stack.pop()
        order.append(v)
        deg[v] = 0
        for dest in adj[v]:
            if deg[dest] > 0:
                parent[v] = dest
                deg[dest] -= 1
                if dest != start and deg[dest] == 1:
                    stack.append(dest)
    return order, parent

def dfs_postorder(adj, root):
    n = len(adj)
    parent = [-1] * n
    order = []
    iters = [iter(adj[u]) for u in range(n)]
    stack = [root]
    visited = set()
    while stack:
        u = stack[-1]
        if u not in visited:
            visited.add(u)
        for v in iters[u]:
            if v != parent[u]:
                parent[v] = u
                stack.append(v)
                break
        else:
            stack.pop()
            order.append(u)
    return parent, order


# ########################################
#
