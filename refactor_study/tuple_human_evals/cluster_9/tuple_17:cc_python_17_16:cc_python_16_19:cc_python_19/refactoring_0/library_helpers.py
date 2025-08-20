# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

# ==== NEW HELPER FUNCTIONS ====
import sys
from collections import deque
from heapq import heappush, heappop

def build_adj_list(n, edges):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj

def dijkstra(adj, src):
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

def recover_path(parent, src, dest):
    if parent[dest] == -1 and dest != src:
        return []
    path = []
    cur = dest
    while cur != -1:
        path.append(cur + 1)
        cur = parent[cur]
    path.reverse()
    return path

def dijkstra_two_step(adj, src):
    INF = 10**18
    n = len(adj)
    dist = [INF]*n
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, v = heappop(heap)
        if d > dist[v]:
            continue
        for u, w1 in adj[v]:
            for x, w2 in adj[u]:
                nd = d + (w1 + w2)**2
                if nd < dist[x]:
                    dist[x] = nd
                    heappush(heap, (nd, x))
    return dist

def build_reverse_graph_for_parity(a):
    n = len(a)
    go = [[] for _ in range(n)]
    sources = []
    dist = [-1]*n
    for i, val in enumerate(a):
        for j in (i - val, i + val):
            if 0 <= j < n:
                if (a[j] % 2) != (val % 2):
                    dist[i] = 1
                    sources.append(i)
                else:
                    go[j].append(i)
    return go, sources, dist

def multi_source_bfs(graph, sources, dist):
    dq = deque(sources)
    while dq:
        u = dq.popleft()
        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                dq.append(v)
    return dist
