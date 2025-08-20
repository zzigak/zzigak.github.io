# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

# ==== NEW HELPER FUNCTIONS ====
def read_ints():
    return list(map(int, input().split()))

def build_adj_undirected(n, edges):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj

def dijkstra(adj, src):
    from heapq import heappush, heappop
    INF = 10**18
    n = len(adj)
    dist = [INF]*n
    parent = [-1]*n
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

def reconstruct_path(parent, dest):
    path = []
    u = dest
    while u != -1:
        path.append(u+1)
        u = parent[u]
    return path[::-1]

def multi_source_bfs(neighbors, sources):
    from collections import deque
    n = len(neighbors)
    dist = [-1]*n
    dq = deque()
    for u in sources:
        if dist[u] == -1:
            dist[u] = 0
            dq.append(u)
    while dq:
        u = dq.popleft()
        for v in neighbors[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                dq.append(v)
    return dist
