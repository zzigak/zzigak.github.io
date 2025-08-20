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
def build_directed_graph(n, edges, reversed=False):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        u0, v0 = u-1, v-1
        if reversed:
            u0, v0 = v0, u0
        adj[u0].append(v0)
    return adj

def _dfs_min(u, adj, colors, container):
    colors[u] = 1
    for v in adj[u]:
        if colors[v] == 1:
            return False
        if colors[v] == 0:
            if not _dfs_min(v, adj, colors, container):
                return False
        container[u] = min(container[u], container[v])
    colors[u] = 2
    return True

def compute_min_reachable(adj):
    n = len(adj)
    container = list(range(n))
    colors = [0] * n
    import sys
    sys.setrecursionlimit(10**7)
    for u in range(n):
        if colors[u] == 0:
            if not _dfs_min(u, adj, colors, container):
                return None
    return container

def build_undirected_graph(n, edges):
    adj = [[] for _ in range(n)]
    edge_set = set()
    for u, v in edges:
        u0, v0 = u-1, v-1
        adj[u0].append(v0)
        adj[v0].append(u0)
        edge_set.add((u0, v0))
        edge_set.add((v0, u0))
    return adj, edge_set

def bfs(n, adj, start):
    from collections import deque
    dist = [-1] * n
    q = deque([start])
    dist[start] = 0
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] < 0:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

def count_nonconnect_pairs(n, edge_set, ds, dt, target):
    cnt = 0
    for u in range(n):
        for v in range(u+1, n):
            if (u, v) not in edge_set:
                if min(ds[u] + dt[v], dt[u] + ds[v]) + 1 >= target:
                    cnt += 1
    return cnt

def _dfs_post(u, adj, seen, order):
    seen[u] = True
    for v in adj[u]:
        if not seen[v]:
            _dfs_post(v, adj, seen, order)
    order.append(u)

def dfs_postorder(n, adj):
    seen = [False] * n
    order = []
    import sys
    sys.setrecursionlimit(10**7)
    for u in range(n):
        if not seen[u]:
            _dfs_post(u, adj, seen, order)
    return order[::-1]

def dfs_mark(start, adj, seen):
    stack = [start]
    if not seen[start]:
        seen[start] = True
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                stack.append(v)
