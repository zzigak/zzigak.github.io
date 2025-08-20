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
        if reversed:
            u, v = v, u
        adj[u-1].append(v-1)
    return adj

def topological_sort(adj):
    from collections import deque
    n = len(adj)
    indeg = [0]*n
    for u in range(n):
        for v in adj[u]:
            indeg[v] += 1
    dq = deque([u for u in range(n) if indeg[u]==0])
    order = []
    while dq:
        u = dq.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                dq.append(v)
    return order if len(order)==n else None

def propagate_min_label(adj, order):
    n = len(adj)
    container = list(range(n))
    for u in reversed(order):
        for v in adj[u]:
            if container[v] < container[u]:
                container[u] = container[v]
    return container

def bfs_distance(adj, start):
    from collections import deque
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

def get_finish_order(adj):
    n = len(adj)
    visited = [False]*n
    order = []
    for u in range(n):
        if not visited[u]:
            stack = [(u,0)]
            while stack:
                v, state = stack.pop()
                if state == 0:
                    if visited[v]:
                        continue
                    visited[v] = True
                    stack.append((v,1))
                    for c in adj[v]:
                        if not visited[c]:
                            stack.append((c,0))
                else:
                    order.append(v)
    return order

def mark_reachable(adj, start, visited):
    stack = [start]
    visited[start] = True
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                stack.append(v)
