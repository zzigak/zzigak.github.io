# ==== NEW HELPER FUNCTIONS ====
from collections import deque

def compute_scc_zero_incoming(E):
    """
    Given directed graph E as adjacency list, compute number of
    strongly connected components with zero incoming edges.
    """
    n = len(E)
    rev = [[] for _ in range(n)]
    for u, vs in enumerate(E):
        for v in vs:
            rev[v].append(u)
    visited = [False] * n
    order = []
    def dfs1(u):
        visited[u] = True
        for v in E[u]:
            if not visited[v]:
                dfs1(v)
        order.append(u)
    for i in range(n):
        if not visited[i]:
            dfs1(i)
    comp = [-1] * n
    cid = 0
    def dfs2(u):
        stack = [u]
        comp[u] = cid
        while stack:
            x = stack.pop()
            for v in rev[x]:
                if comp[v] == -1:
                    comp[v] = cid
                    stack.append(v)
    for u in reversed(order):
        if comp[u] == -1:
            dfs2(u)
            cid += 1
    has_in = [False] * cid
    for u in range(n):
        for v in E[u]:
            if comp[u] != comp[v]:
                has_in[comp[v]] = True
    return has_in.count(False)