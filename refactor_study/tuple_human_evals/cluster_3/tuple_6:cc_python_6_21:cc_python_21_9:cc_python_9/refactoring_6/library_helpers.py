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
        u, v = map(int, input().split())
        u -= offset; v -= offset
        adj[u].append(v)
        adj[v].append(u)
    return adj

def read_weighted_tree(n, offset=1):
    adj = [[] for _ in range(n)]
    for _ in range(n-1):
        u, v, c = map(int, input().split())
        u -= offset; v -= offset
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
        for x in adj[u]:
            v = x[0] if isinstance(x, tuple) else x
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

def max_path_gas(w, adj):
    par, order = parorder(adj, 0)
    n = len(adj)
    f = [0] * n
    best = 0
    for u in reversed(order):
        contribs = []
        for v, c in adj[u]:
            if v == par[u]: continue
            d = f[v] - c
            if d > 0: contribs.append(d)
        contribs.sort(reverse=True)
        a = contribs[0] if contribs else 0
        b = contribs[1] if len(contribs) > 1 else 0
        f[u] = w[u] + a
        best = max(best, w[u] + a + b)
    return best

def max_beavers(beaver, adj, start):
    from collections import deque
    n = len(adj)
    deg = [len(adj[i]) for i in range(n)]
    deg[start] += n
    if n == 1:
        return 0
    dp = [0] * n
    stack = deque(i for i in range(n) if i != start and deg[i] == 1)
    while stack:
        v = stack.popleft()
        deg[v] = 0
        childs = []
        child_dp = []
        for nei in adj[v]:
            if deg[nei] == 0:
                childs.append(nei)
                child_dp.append(dp[nei])
            else:
                deg[nei] -= 1
                if nei != start and deg[nei] == 1:
                    stack.append(nei)
        child_dp.sort(reverse=True)
        x = min(beaver[v] - 1, len(childs))
        dp[v] = 1 + sum(child_dp[:x]) + x
        beaver[v] -= x + 1
        for c in childs:
            y = min(beaver[v], beaver[c])
            beaver[v] -= y
            dp[v] += 2 * y
    child_dp = [dp[c] for c in adj[start]]
    child_dp.sort(reverse=True)
    x = min(beaver[start], len(adj[start]))
    ans = sum(child_dp[:x]) + x
    beaver[start] -= x
    for c in adj[start]:
        y = min(beaver[start], beaver[c])
        beaver[start] -= y
        ans += 2 * y
    return ans

def max_product_components(adj, root=0):
    from fractions import Fraction
    par, order = parorder(adj, root)
    children = get_children(par)
    n = len(adj)
    H = [0] * n
    F = [0] * n
    FoH = [[] for _ in range(n)]
    for u in reversed(order):
        F_u = 1
        ratios = []
        for v in children[u]:
            F_u *= H[v]
            ratios.append(F[v] / H[v])
        F[u] = F_u
        ratios.sort(reverse=True)
        FoH[u] = ratios
        ans = F_u
        pd = 1; cnt = 0
        for x in ratios:
            pd *= x; cnt += 1
            ans = max(ans, int(pd * F_u) * (cnt + 1))
        for v in children[u]:
            pd = 1; cnt = 0
            for x in FoH[v]:
                pd *= x; cnt += 1
                val = int(pd * (F_u * F[v])) // H[v] * (cnt + 2)
                ans = max(ans, val)
        H[u] = ans
    return H[root]
