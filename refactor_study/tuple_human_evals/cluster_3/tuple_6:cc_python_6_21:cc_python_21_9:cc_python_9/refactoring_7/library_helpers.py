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

def get_postorder(adj, root):
    n = len(adj)
    parent = [-1] * n
    order = []
    stack = [(root, -1, False)]
    while stack:
        u, p, done = stack.pop()
        if done:
            order.append(u)
        else:
            parent[u] = p
            stack.append((u, p, True))
            for w in adj[u]:
                v = w if isinstance(w, int) else w[0]
                if v != p:
                    stack.append((v, u, False))
    return parent, order

def read_weighted_tree(n, offset=1):
    adj = [[] for _ in range(n)]
    for _ in range(n-1):
        u, v, c = read_ints()
        if offset:
            u -= 1; v -= 1
        adj[u].append((v, c))
        adj[v].append((u, c))
    return adj

def compute_muncher(adj, beaver, start):
    from collections import deque
    n = len(adj)
    deg = [len(adj[i]) for i in range(n)]
    deg[start] += n + 5
    if n == 1:
        return 0
    dp = [0] * n
    queue = deque([i for i in range(n) if i != start and deg[i] == 1])
    while queue:
        v = queue.popleft()
        deg[v] = 0
        childs = []
        for u in adj[v]:
            if deg[u] == 0:
                childs.append(u)
            else:
                deg[u] -= 1
                if deg[u] == 1:
                    queue.append(u)
        child_dp = sorted((dp[c] for c in childs), reverse=True)
        x = min(beaver[v] - 1, len(childs))
        cur = 1 + sum(child_dp[:x]) + x
        beaver[v] -= x + 1
        for c in childs:
            t = min(beaver[v], beaver[c])
            beaver[v] -= t
            cur += 2 * t
        dp[v] = cur
    # at start
    childs = adj[start]
    child_dp = sorted((dp[c] for c in childs), reverse=True)
    x = min(beaver[start], len(childs))
    ans = sum(child_dp[:x]) + x
    beaver[start] -= x
    for c in childs:
        t = min(beaver[start], beaver[c])
        beaver[start] -= t
        ans += 2 * t
    return ans

def max_product_components(adj, root=0):
    parent, order = get_postorder(adj, root)
    n = len(adj)
    f = [None] * n
    for u in order:
        d = {1: 1}
        for v in adj[u]:
            if v == parent[u]:
                continue
            dv = f[v]
            nd = {}
            for s1, p1 in d.items():
                for s2, p2 in dv.items():
                    # keep edge
                    s = s1 + s2
                    pd = p1 * p2
                    if nd.get(s, 0) < pd:
                        nd[s] = pd
                    # cut edge
                    s = s1
                    pd = p1 * p2 * s2
                    if nd.get(s, 0) < pd:
                        nd[s] = pd
            d = nd
        f[u] = d
    res = 0
    for s, p in f[root].items():
        v = p * s
        if v > res:
            res = v
    return res
