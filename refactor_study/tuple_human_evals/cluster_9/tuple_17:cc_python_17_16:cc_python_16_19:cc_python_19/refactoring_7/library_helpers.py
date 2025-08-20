# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

# ==== NEW HELPER FUNCTIONS ====
import sys
from heapq import heappush, heappop
from collections import deque

def read_ints():
    return map(int, sys.stdin.readline().split())

def build_adj_undirected(n, edges):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj

def dijkstra(adj, src, n, dest=None):
    INF = 10**30
    dist = [INF] * n
    parent = [-1] * n
    dist[src] = 0
    pq = []
    heappush(pq, (0, src))
    while pq:
        d, u = heappop(pq)
        if d > dist[u]:
            continue
        if dest is not None and u == dest:
            break
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heappush(pq, (nd, v))
    return (dist, parent) if dest is not None else dist

def reconstruct_path(parent, src, dest):
    path = []
    u = dest
    while u != -1:
        path.append(u + 1)
        u = parent[u]
    return list(reversed(path))

def dijkstra_dynamic(n, src, get_neighbors):
    INF = 10**30
    dist = [INF] * n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heappop(pq)
        if d > dist[u]:
            continue
        for v, w in get_neighbors(u):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heappush(pq, (nd, v))
    return dist

def multi_source_bfs(adj_rev, sources, n):
    INF = 10**30
    dist = [INF] * n
    dq = deque()
    for s in sources:
        dist[s] = 0
        dq.append(s)
    while dq:
        u = dq.popleft()
        for v in adj_rev[u]:
            if dist[v] == INF:
                dist[v] = dist[u] + 1
                dq.append(v)
    return dist

def build_reverse_graph(a):
    n = len(a)
    adj_rev = [[] for _ in range(n)]
    sources = []
    for i, ai in enumerate(a):
        for ni in (i - ai, i + ai):
            if 0 <= ni < n:
                if a[ni] % 2 != ai % 2:
                    sources.append(i)
                else:
                    adj_rev[ni].append(i)
    return adj_rev, sources
