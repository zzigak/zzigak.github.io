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
        if not offset:
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

def compute_depth(par, order):
    depth = [0] * len(par)
    for u in order[1:]:
        depth[u] = depth[par[u]] + 1
    return depth

def compute_subtree_sizes(par, order):
    n = len(par)
    subtree = [1] * n
    for u in reversed(order[1:]):
        subtree[par[u]] += subtree[u]
    return subtree

def merge_dp_interval(dp_p, dp_c, l_p, r_p, l_c, r_c):
    add0 = max(dp_c[0] + abs(l_p - l_c), dp_c[1] + abs(l_p - r_c))
    add1 = max(dp_c[0] + abs(r_p - l_c), dp_c[1] + abs(r_p - r_c))
    dp_p[0] += add0
    dp_p[1] += add1

def merge_dp_diameter(dp_p, dp_c, K, mod):
    m = max(len(dp_p), len(dp_c) + 1)
    res = [0] * m
    for i in range(len(dp_p)):
        for j in range(len(dp_c)):
            ways = dp_p[i] * dp_c[j] % mod
            # cut edge
            res[i] = (res[i] + ways) % mod
            # keep edge if diameter ok
            if i + j + 1 <= K:
                idx = i if i >= j + 1 else j + 1
                res[idx] = (res[idx] + ways) % mod
    return res
