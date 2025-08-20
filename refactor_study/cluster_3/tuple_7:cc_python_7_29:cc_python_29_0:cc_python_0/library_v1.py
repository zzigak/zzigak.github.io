# ########## LIBRARY HELPERS ##########

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

def tree_dp_down(adj, root, val):
    par,order = parorder(adj,root)
    dp = val.copy()
    for u in reversed(order):
        for v in adj[u]:
            if v!=par[u] and dp[v]>0:
                dp[u] += dp[v]
    return dp, par, order

def tree_reroot(adj, root, dp, par, order):
    ans = dp.copy()
    for u in order:
        for v in adj[u]:
            if v!=par[u]:
                up = ans[u] - max(0, dp[v])
                ans[v] = dp[v] + max(0, up)
    return ans

def compute_min_moves(v, adj, root=1):
    par, order = parorder(adj, root)
    n = len(adj)
    plus = [0]*n; minus=[0]*n
    for x in reversed(order):
        p=par[x]
        if p>=0:
            z = v[x] + minus[x] - plus[x]
            plus[p] = max(plus[p], plus[x] + max(z,0))
            minus[p] = max(minus[p], minus[x] + max(-z,0))
    return plus[root] + minus[root]

def propagate_diff(diff, parent, k):
    for i in range(len(diff)-1,1,-1):
        p = parent[i]
        if diff[i]>=0:
            diff[p] += diff[i]
        else:
            diff[p] += diff[i] * k[i]
            if diff[p] < -10**17:
                return False
    return diff[1] >= 0


# ########################################
#
