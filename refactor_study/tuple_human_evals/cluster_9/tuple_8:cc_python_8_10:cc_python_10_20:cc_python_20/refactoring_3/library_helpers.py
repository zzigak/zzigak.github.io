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

def build_graph(n, edges, reversed=False):
    gp = [[] for _ in range(n)]
    for u, v in edges:
        if reversed:
            gp[v-1].append(u-1)
        else:
            gp[u-1].append(v-1)
    return gp

def compute_reach_min(n, edges):
    visited = [False]*n
    colors = {}
    container = list(range(n))
    for s in range(n):
        if not visited[s]:
            stack = [s]
            while stack:
                v = stack.pop()
                if colors.get(v,0) == 0:
                    colors[v] = 1
                    stack.append(v)
                    for c in edges[v]:
                        if colors.get(c,0) == 1:
                            return None
                        if not visited[c] and colors.get(c,0) == 0:
                            stack.append(c)
                else:
                    tmp = [container[c] for c in edges[v]]
                    if tmp:
                        container[v] = min(min(tmp), container[v])
                    colors[v] = 2
                    visited[v] = True
    return container

def bfs_distance(adj, start):
    INF = float('inf')
    n = len(adj)
    dist = [INF]*n
    dist[start] = 0
    dq = deque([start])
    while dq:
        u = dq.popleft()
        for v in adj[u]:
            if dist[v] > dist[u] + 1:
                dist[v] = dist[u] + 1
                dq.append(v)
    return dist

def build_adj_undirected(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u-1].append(v-1)
        adj[v-1].append(u-1)
    return adj

def dfs_postorder(u, edges, visited, order):
    visited[u] = True
    for v in edges[u]:
        if not visited[v]:
            dfs_postorder(v, edges, visited, order)
    order.append(u)

def compute_postorder(n, edges):
    visited = [False]*n
    order = []
    for i in range(n):
        if not visited[i]:
            dfs_postorder(i, edges, visited, order)
    return order[::-1]

def dfs_mark(start, edges, visited):
    stack = [start]
    while stack:
        u = stack.pop()
        if not visited[u]:
            visited[u] = True
            for v in edges[u]:
                if not visited[v]:
                    stack.append(v)
