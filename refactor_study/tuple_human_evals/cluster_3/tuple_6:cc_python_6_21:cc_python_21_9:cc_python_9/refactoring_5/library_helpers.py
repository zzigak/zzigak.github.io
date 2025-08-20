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
from collections import deque
from fractions import Fraction

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

def read_weighted_tree(n, offset=0):
    adj = [[] for _ in range(n + (1 if offset else 0))]
    for _ in range(n - 1):
        u, v, c = read_ints()
        if offset == 0:
            u -= 1; v -= 1
        adj[u].append((v, c))
        adj[v].append((u, c))
    return adj

def compute_max_gas(w, adj):
    n = len(adj)
    deg = [len(adj[i]) for i in range(n)]
    z = [[0] for _ in range(n)]
    q = deque()
    for i in range(n):
        if deg[i] == 1:
            q.append((i, 0))
    m = 0
    while q:
        x, y = q.popleft()
        if deg[x] == 0: continue
        for t, c in adj[x]:
            if deg[t] > 0:
                z[t].append(y + w[x] - c)
                deg[t] -= 1
                if deg[t] == 1:
                    q.append((t, max(z[t])))
                break
        deg[x] = 0
    for i in range(n):
        zs = sorted(z[i])
        if zs:
            m = max(m, w[i] + zs[-1])
        if len(zs) >= 2:
            m = max(m, w[i] + zs[-1] + zs[-2])
    return m

def compute_max_beaver(n, beaver, adj, start):
    deg = [len(adj[i]) for i in range(n)]
    deg[start] += n + 5
    if n == 1: return 0
    dp = [0]*n
    stack = [i for i in range(n) if i != start and deg[i] == 1]
    while stack:
        v = stack.pop()
        deg[v] = 0
        child = []
        for u in adj[v]:
            if deg[u] == 0:
                child.append(u)
            else:
                deg[u] -= 1
                if deg[u] == 1:
                    stack.append(u)
        child_dp = sorted((dp[c] for c in child), reverse=True)
        x = min(beaver[v] - 1, len(child))
        dp[v] = 1 + sum(child_dp[:x]) + x
        beaver[v] -= x + 1
        for c in child:
            y = min(beaver[v], beaver[c])
            beaver[v] -= y
            dp[v] += 2*y
    neigh = adj[start]
    child_dp = sorted((dp[v] for v in neigh), reverse=True)
    x = min(beaver[start], len(neigh))
    ans = sum(child_dp[:x]) + x
    beaver[start] -= x
    for c in neigh:
        y = min(beaver[start], beaver[c])
        beaver[start] -= y
        ans += 2*y
    return ans

def get_post_order(adj, root=0):
    parent = [-1]*len(adj)
    order = []
    stack = [(root, iter(adj[root]))]
    while stack:
        u, it = stack[-1]
        for v in it:
            if v != parent[u]:
                parent[v] = u
                stack.append((v, iter(adj[v])))
                break
        else:
            stack.pop()
            order.append(u)
    return parent, order

def get_children(parent):
    children = [[] for _ in parent]
    for u, p in enumerate(parent):
        if p >= 0:
            children[p].append(u)
    return children

def compute_max_product(adj, root=0):
    parent, post = get_post_order(adj, root)
    children = get_children(parent)
    n = len(adj)
    H = [0]*n
    F = [0]*n
    FoH = [[] for _ in range(n)]
    for u in post:
        F_u = 1
        for v in children[u]:
            F_u *= H[v]
        F[u] = F_u
        lst = []
        for v in children[u]:
            if H[v] > 0:
                lst.append(F[v]/H[v])
        FoH[u] = sorted(lst, reverse=True)
        ans = F_u
        pd = Fraction(1, 1)
        for idx, frac in enumerate(FoH[u]):
            pd *= frac
            k = idx + 1
            val = pd * F_u * (k+1)
            ans = max(ans, int(val))
        for v in children[u]:
            pd2 = Fraction(1, 1)
            base = F_u * (F[v]/H[v])
            for idx, frac in enumerate(FoH[v]):
                pd2 *= frac
                k = idx + 1
                val = pd2 * base * (k+2)
                ans = max(ans, int(val))
        H[u] = ans
    return H[root]
