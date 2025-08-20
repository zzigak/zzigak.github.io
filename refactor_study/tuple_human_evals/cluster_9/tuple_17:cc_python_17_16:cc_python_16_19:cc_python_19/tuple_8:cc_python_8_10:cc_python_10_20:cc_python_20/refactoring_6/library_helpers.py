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
def build_adj_directed(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    return adj

def build_adj_undirected(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    return adj

def reverse_graph(graph):
    n = len(graph)
    rg = [[] for _ in range(n)]
    for u, nbrs in enumerate(graph):
        for v in nbrs:
            rg[v].append(u)
    return rg

def bfs(start, graph):
    from collections import deque
    n = len(graph)
    dist = [-1]*n
    q = deque([start]); dist[start] = 0
    while q:
        u = q.popleft()
        for v in graph[u]:
            if dist[v] < 0:
                dist[v] = dist[u] + 1; q.append(v)
    return dist

def dfs_min(u, graph, state, ans):
    state[u] = 1
    for v in graph[u]:
        if state[v] == 1:
            return False
        if state[v] == 0:
            if not dfs_min(v, graph, state, ans):
                return False
        if ans[v] < ans[u]:
            ans[u] = ans[v]
    state[u] = 2
    return True

def compute_min_reachable(graph):
    n = len(graph)
    state = [0]*n
    ans = list(range(n))
    for u in range(n):
        if state[u] == 0:
            if not dfs_min(u, graph, state, ans):
                return None
    return ans

def dfs_finish(u, graph, visited, order):
    visited[u] = True
    for v in graph[u]:
        if not visited[v]:
            dfs_finish(v, graph, visited, order)
    order.append(u)

def dfs_finish_order(graph):
    n = len(graph)
    visited = [False]*n
    order = []
    for u in range(n):
        if not visited[u]:
            dfs_finish(u, graph, visited, order)
    return order

def dfs_mark(start, graph, visited):
    stack = [start]
    while stack:
        u = stack.pop()
        if not visited[u]:
            visited[u] = True
            for v in graph[u]:
                if not visited[v]:
                    stack.append(v)
