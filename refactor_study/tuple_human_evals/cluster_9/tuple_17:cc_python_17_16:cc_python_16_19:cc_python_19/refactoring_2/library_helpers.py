# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

# ==== NEW HELPER FUNCTIONS ====
from collections import defaultdict, deque
from heapq import heappush, heappop

def build_undirected_adj(n, edges):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj

def dijkstra(adj, src):
    n = len(adj)
    dist = [float('inf')] * n
    parent = [-1] * n
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, u = heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heappush(heap, (nd, v))
    return dist, parent

def reconstruct_path(parent, src, dest):
    path = []
    u = dest
    while u != -1:
        path.append(u)
        u = parent[u]
    if not path or path[-1] != src:
        return []
    return path[::-1]

def multi_source_bfs(adj, sources):
    n = len(adj)
    dist = [-1] * n
    q = deque()
    for v, d in sources:
        if dist[v] == -1 or d < dist[v]:
            dist[v] = d
            q.append(v)
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

def two_edge_dijkstra(adj):
    inf = 10**30
    n = len(adj)
    dist = [inf] * n
    td = [0] * n
    dist[0] = 0
    heap = [(0, 0)]
    while heap:
        d, u = heappop(heap)
        if d > dist[u]:
            continue
        mids = []
        for v, w in adj[u]:
            td[v] = w
            mids.append(v)
        for v in mids:
            w1 = td[v]
            for x, w2 in adj[v]:
                nd = d + (w1 + w2) ** 2
                if nd < dist[x]:
                    dist[x] = nd
                    heappush(heap, (nd, x))
    for i in range(n):
        if dist[i] >= inf:
            dist[i] = -1
    return dist
