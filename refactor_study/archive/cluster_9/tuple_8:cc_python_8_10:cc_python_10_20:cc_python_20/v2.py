# ########## LIBRARY HELPERS ##########

# ==== RETRIEVED HELPER FUNCTIONS ====
def dijkstra_dist(adj, s):
    # Success rate: 1/1

    import heapq
    INF = 10 ** 18
    n = len(adj)
    dist = [INF] * n
    dist[s] = 0
    heap = [(0, s)]
    while heap:
        (d, u) = heapq.heappop(heap)
        if d != dist[u]:
            continue
        for (v, w) in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist

def multi_source_bfs(neighbors, sources):
    # Success rate: 0.0/0
    n = len(neighbors)
    dist = [-1] * n
    q = [0] * n
    head = tail = 0
    for u in sources:
        if dist[u] < 0:
            dist[u] = 0
            q[tail] = u
            tail += 1
    while head < tail:
        u = q[head]
        head += 1
        du = dist[u] + 1
        for v in neighbors[u]:
            if dist[v] < 0:
                dist[v] = du
                q[tail] = v
                tail += 1
    return dist

def build_weighted_graph(n, edges):
    # Success rate: 1/1

    gp = [dict() for _ in range(n)]
    for (u, v, w) in edges:
        if v not in gp[u] or w < gp[u][v]:
            gp[u][v] = w
        if u not in gp[v] or w < gp[v][u]:
            gp[v][u] = w
    adj = [[] for _ in range(n)]
    for u in range(n):
        for (v, w) in gp[u].items():
            adj[u].append((v, w))
    return adj

def bfs_distance(adj, start):
    # Success rate: 2/2

    from collections import deque
    INF = float('inf')
    n = len(adj)
    dist = [INF] * n
    dist[start] = 0
    dq = deque([start])
    while dq:
        u = dq.popleft()
        for v in adj[u]:
            if dist[v] > dist[u] + 1:
                dist[v] = dist[u] + 1
                dq.append(v)
    return dist

def dijkstra(adj, src):
    # Success rate: 3/3

    from heapq import heappush, heappop
    INF = 10 ** 18
    n = len(adj)
    dist = [INF] * n
    parent = [-1] * n
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        (d, u) = heappop(heap)
        if d > dist[u]:
            continue
        for (v, w) in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heappush(heap, (nd, v))
    return (dist, parent)

def build_adj_undirected(n, edges):
    # Success rate: 4/4

    adj = [[] for _ in range(n)]
    for (u, v, w) in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj

def compute_min_reachable(adj, dist):
    # Success rate: 1/1

    n = len(adj)
    nodes = list(range(n))
    nodes.sort(key=lambda x: dist[x], reverse=True)
    ans = [0] * n
    for u in nodes:
        best = dist[u]
        for v in adj[u]:
            if dist[v] > dist[u]:
                best = min(best, ans[v])
            else:
                best = min(best, dist[v])
        ans[u] = best
    return ans


# ==== NEW HELPER FUNCTIONS ====
from collections import deque

def build_dir_graph(n, edges, rev=False):
    g = [[] for _ in range(n)]
    for u, v in edges:
        if rev: u, v = v, u
        g[u].append(v)
    return g

def build_undir_graph(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)
    return g

def get_topo_order(n, adj):
    indeg = [0] * n
    for u in range(n):
        for v in adj[u]:
            indeg[v] += 1
    dq = deque(u for u in range(n) if indeg[u] == 0)
    order = []
    while dq:
        u = dq.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                dq.append(v)
    return order if len(order) == n else None

def compute_min_dag(n, adj, topo):
    container = list(range(n))
    for u in reversed(topo):
        for v in adj[u]:
            if container[v] < container[u]:
                container[u] = container[v]
    return container

def dfs_order(u, g, visited, order):
    visited[u] = True
    for v in g[u]:
        if not visited[v]:
            dfs_order(v, g, visited, order)
    order.append(u)

def assign_component(u, rg, comp, cid):
    comp[u] = cid
    for v in rg[u]:
        if comp[v] < 0:
            assign_component(v, rg, comp, cid)

def kosaraju_scc(n, edges):
    g = build_dir_graph(n, edges, rev=False)
    visited = [False] * n
    order = []
    for u in range(n):
        if not visited[u]:
            dfs_order(u, g, visited, order)
    rg = build_dir_graph(n, edges, rev=True)
    comp = [-1] * n
    cid = 0
    for u in reversed(order):
        if comp[u] < 0:
            assign_component(u, rg, comp, cid)
            cid += 1
    return comp, cid

def count_new_roads_to_connect(n, edges, comp, comp_count, s):
    comp_adj = [set() for _ in range(comp_count)]
    for u, v in edges:
        cu, cv = comp[u], comp[v]
        if cu != cv:
            comp_adj[cu].add(cv)
    start = comp[s]
    dq = deque([start])
    vis = [False] * comp_count
    vis[start] = True
    while dq:
        u = dq.popleft()
        for v in comp_adj[u]:
            if not vis[v]:
                vis[v] = True
                dq.append(v)
    not_reached = [u for u in range(comp_count) if not vis[u]]
    indeg = [0] * comp_count
    for u in not_reached:
        for v in comp_adj[u]:
            if not vis[v]:
                indeg[v] += 1
    return sum(1 for u in not_reached if indeg[u] == 0)


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_10:cc_python_10 ##########

from codebank import *

def main():
    n, m, s, t = map(int, input().split())
    s -= 1; t -= 1
    edges = []
    for _ in range(m):
        u, v = map(int, input().split())
        edges.append((u-1, v-1))
    adj = build_undir_graph(n, edges)
    ds = bfs_distance(adj, s)
    dt = bfs_distance(adj, t)
    d_st = ds[t]
    exist = [set() for _ in range(n)]
    for u, v in edges:
        exist[u].add(v)
        exist[v].add(u)
    ans = 0
    for u in range(n):
        for v in range(u+1, n):
            if v not in exist[u] and min(ds[u] + dt[v], dt[u] + ds[v]) + 1 >= d_st:
                ans += 1
    print(ans)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_20:cc_python_20 ##########

from codebank import *

def main():
    import sys
    sys.setrecursionlimit(10000)
    n, m, s = map(int, sys.stdin.readline().split())
    s -= 1
    edges = []
    for _ in range(m):
        u, v = map(int, sys.stdin.readline().split())
        edges.append((u-1, v-1))
    comp, cnt = kosaraju_scc(n, edges)
    ans = count_new_roads_to_connect(n, edges, comp, cnt, s)
    print(ans)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_8:cc_python_8 ##########

from codebank import *

def main():
    import sys
    data = sys.stdin.readline
    n, m = map(int, data().split())
    edges = []
    for _ in range(m):
        u, v = map(int, data().split())
        edges.append((u-1, v-1))
    g = build_dir_graph(n, edges)
    topo = get_topo_order(n, g)
    if topo is None:
        print(-1)
        return
    fwd = compute_min_dag(n, g, topo)
    gr = build_dir_graph(n, edges, rev=True)
    topo2 = get_topo_order(n, gr)
    back = compute_min_dag(n, gr, topo2)
    container = [fwd[i] if fwd[i] < back[i] else back[i] for i in range(n)]
    res = sum(1 for i in range(n) if container[i] == i)
    s = ''.join('A' if container[i] == i else 'E' for i in range(n))
    print(res)
    print(s)

if __name__ == "__main__":
    main()
