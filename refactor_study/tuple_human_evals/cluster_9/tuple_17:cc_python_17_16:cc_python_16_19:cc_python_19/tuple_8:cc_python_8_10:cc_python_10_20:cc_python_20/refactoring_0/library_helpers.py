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
def build_adj(n, edges, directed=True):
    adj=[[] for _ in range(n)]
    if directed:
        for u,v in edges:
            adj[u].append(v)
    else:
        for u,v in edges:
            adj[u].append(v)
            adj[v].append(u)
    return adj

def reverse_adj(adj):
    n=len(adj)
    radj=[[] for _ in range(n)]
    for u,vs in enumerate(adj):
        for v in vs:
            radj[v].append(u)
    return radj

def bfs(start, adj):
    from collections import deque
    n=len(adj)
    dist=[-1]*n
    q=deque([start])
    dist[start]=0
    while q:
        u=q.popleft()
        for v in adj[u]:
            if dist[v]<0:
                dist[v]=dist[u]+1
                q.append(v)
    return dist

def dfs_min_visit(u, adj, visited, colors, container):
    colors[u]=1
    for v in adj[u]:
        if colors[v]==1:
            return False
        if not visited[v]:
            if not dfs_min_visit(v, adj, visited, colors, container):
                return False
        container[u]=min(container[u], container[v])
    colors[u]=2
    visited[u]=True
    return True

def compute_min_reachable(adj):
    n=len(adj)
    visited=[False]*n
    colors=[0]*n
    container=list(range(n))
    for u in range(n):
        if not visited[u]:
            if not dfs_min_visit(u, adj, visited, colors, container):
                return None
    return container

def dfs_finish(u, adj, visited, order):
    visited[u]=True
    for v in adj[u]:
        if not visited[v]:
            dfs_finish(v, adj, visited, order)
    order.append(u)

def topo_sort(adj):
    n=len(adj)
    visited=[False]*n
    order=[]
    for u in range(n):
        if not visited[u]:
            dfs_finish(u, adj, visited, order)
    return order[::-1]
