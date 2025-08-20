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
import sys
from collections import deque
from fractions import Fraction

def read_ints():
    return list(map(int, sys.stdin.readline().split()))

def read_tree(n, offset=0):
    adj=[[] for _ in range(n+offset)]
    cost={}
    for _ in range(n-1):
        u,v,c=read_ints()
        if offset==0:
            u-=1; v-=1
        adj[u].append((v,c))
        adj[v].append((u,c))
        cost[(u,v)]=c; cost[(v,u)]=c
    return adj, cost

def parorder(adj, root):
    par=[None]*len(adj)
    par[root]=-1
    stack=[root]
    order=[]
    visited={root}
    while stack:
        u=stack.pop()
        order.append(u)
        for v in adj[u]:
            vv=v[0] if isinstance(v, tuple) else v
            if vv not in visited:
                visited.add(vv)
                par[vv]=u
                stack.append(v)
    return par, order

def get_children(par):
    children=[[] for _ in par]
    for u,p in enumerate(par):
        if p is not None and p>=0:
            children[p].append(u)
    return children

def max_path_gain(weights, adj, cost, root=0):
    par, order = parorder(adj, root)
    dp = [0]*len(adj)
    ans = 0
    for u in reversed(order):
        best = []
        for v,c in adj[u]:
            if par[v]==u:
                val = dp[v] - c + weights[v]
                if val>0:
                    best.append(val)
        best.sort(reverse=True)
        if best:
            dp[u] = best[0]
        curr = weights[u] + sum(best[:2])
        if curr>ans:
            ans = curr
    return ans

def dfs_order(adj, root=0):
    par = [-1]*len(adj)
    order = []
    stack = [(root, False)]
    while stack:
        u, vis = stack.pop()
        if not vis:
            stack.append((u, True))
            for v in adj[u]:
                if v!=par[u]:
                    par[v]=u
                    stack.append((v, False))
        else:
            order.append(u)
    return par, order

def solve_node(u, adj, par, H, F):
    fracs=[]
    F[u]=1
    for v in adj[u]:
        if v!=par[u]:
            F[u] *= H[v]
            fracs.append(Fraction(F[v], H[v]))
    ans = F[u]
    fracs.sort(reverse=True)
    pd = Fraction(1,1)
    for i, x in enumerate(fracs):
        pd *= x
        cand = int(pd * F[u]) * (i+2)
        if cand>ans:
            ans = cand
    for v in adj[u]:
        if v!=par[u]:
            pd2 = Fraction(1,1)
            fr2=[]
            for w in adj[v]:
                if w!=u:
                    fr2.append(Fraction(F[w], H[w]))
            fr2.sort(reverse=True)
            for i, x in enumerate(fr2):
                pd2 *= x
                val = int(pd2 * F[u] * F[v] / H[v]) * (i+3)
                if val>ans:
                    ans = val
    H[u] = ans
