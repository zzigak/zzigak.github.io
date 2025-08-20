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
    for _ in range(n-1):
        u, v = map(int, input().split())
        if offset == 0:
            u -= 1; v -= 1
        adj[u].append(v)
        adj[v].append(u)
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

def compute_depths(par, order):
    depth = [0] * len(par)
    for v in order:
        p = par[v]
        if p != -1:
            depth[v] = depth[p] + 1
    return depth

def subtree_sizes(par, order):
    sizes = [1] * len(par)
    for v in reversed(order):
        p = par[v]
        if p != -1:
            sizes[p] += sizes[v]
    return sizes

def get_children(par):
    children = [[] for _ in par]
    for u, p in enumerate(par):
        if p >= 0:
            children[p].append(u)
    return children

def compute_contrib(dp_child, parent_val, child_L, child_R):
    return max(dp_child[0] + abs(parent_val - child_L),
               dp_child[1] + abs(parent_val - child_R))

def merge_dp(dp_v, dp_child, K, mod):
    res = [0] * max(len(dp_v), len(dp_child) + 1)
    for i, a in enumerate(dp_v):
        for j, b in enumerate(dp_child):
            if i + j + 1 <= K:
                idx = max(i, j + 1)
                res[idx] = (res[idx] + a * b) % mod
            res[i] = (res[i] + a * b) % mod
    return res
